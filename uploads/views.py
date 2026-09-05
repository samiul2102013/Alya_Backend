import os
import shutil
import uuid
from datetime import datetime, timezone

from django.conf import settings
from django.db import transaction
from rest_framework import status as drf_status
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import MediaItem
from .models import UploadSession


def _tmp_dir(file_id):
    return os.path.join(
        settings.MEDIA_ROOT,
        getattr(settings, 'UPLOAD_CHUNK_TMP_SUBDIR', 'uploads/tmp'),
        str(file_id),
    )


def _final_dir():
    base = settings.MEDIA_ROOT
    sub = getattr(settings, 'UPLOAD_FINAL_SUBDIR', 'uploads')
    today = datetime.now(timezone.utc)
    target = os.path.join(base, sub, f'{today.year:04d}', f'{today.month:02d}')
    os.makedirs(target, exist_ok=True)
    return target


def _safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class ChunkedUploadView(APIView):
    """POST /api/uploads

    Accepts a single chunk of a chunked upload. Two calling styles:

    1. Resume mode (recommended): the client sends `file_id`, `chunk_index`,
       `total_chunks`, `filename`, and the multipart `chunk` file. The server
       creates an UploadSession if `file_id` is new, then writes the chunk to
       MEDIA_ROOT/uploads/tmp/<file_id>/<chunk_index>.

    2. Simple single-shot: just send a `file` field. Treated like a single
       chunk (`total_chunks=1`). Kept for backward compatibility with the
       original /uploads contract.

    Auth: open in dev (no auth) so the legacy call still works; in production
    the page wraps it with the admin auth header.
    """

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]

    def post(self, request):
        max_bytes = int(getattr(settings, 'MAX_UPLOAD_SIZE_BYTES', 5 * 1024 * 1024 * 1024))

        # --- Simple single-shot mode ---
        file_obj = request.FILES.get('file')
        file_id = request.data.get('file_id')

        if file_obj and not file_id:
            return self._single_shot(file_obj, max_bytes)

        if not file_id:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'FILE_REQUIRED',
                        'message': 'Provide a `file` field (single-shot) or a `file_id` + `chunk` (chunked).',
                        'details': {},
                    },
                },
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        # --- Chunked mode ---
        chunk = request.FILES.get('chunk')
        chunk_index = _safe_int(request.data.get('chunk_index'), -1)
        total_chunks = max(_safe_int(request.data.get('total_chunks'), 0), 1)
        filename = request.data.get('filename') or (chunk.name if chunk else 'upload.bin')

        if chunk is None or chunk_index < 0:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'CHUNK_REQUIRED',
                        'message': 'Provide `chunk` file and `chunk_index`.',
                        'details': {},
                    },
                },
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        try:
            session = UploadSession.objects.get(file_id=file_id)
        except (UploadSession.DoesNotExist, ValueError):
            session = UploadSession.objects.create(
                filename=filename,
                mime_type=request.data.get('mime_type') or (chunk.content_type if chunk else ''),
                total_chunks=total_chunks,
                uploaded_by=str(getattr(request.user, 'email', '')) if getattr(request, 'user', None) and request.user.is_authenticated else '',
            )

        if session.status != 'pending':
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'SESSION_CLOSED',
                        'message': f'Upload session is {session.status}.',
                        'details': {},
                    },
                },
                status=drf_status.HTTP_409_CONFLICT,
            )

        # Per-chunk cap: must fit in the configured memory threshold.
        per_chunk_cap = int(getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 50 * 1024 * 1024))
        if chunk.size > per_chunk_cap:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'CHUNK_TOO_LARGE',
                        'message': f'Chunk size {chunk.size} exceeds per-chunk cap {per_chunk_cap}.',
                        'details': {},
                    },
                },
                status=drf_status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )

        tmp = _tmp_dir(session.file_id)
        os.makedirs(tmp, exist_ok=True)
        chunk_path = os.path.join(tmp, f'{chunk_index:06d}.part')
        with open(chunk_path, 'wb') as f:
            for piece in chunk.chunks():
                f.write(piece)

        received = list(session.received_chunks or [])
        if chunk_index not in received:
            received.append(chunk_index)
            session.received_chunks = received
            session.total_size = (session.total_size or 0) + chunk.size
            session.save(update_fields=['received_chunks', 'total_size', 'updated_at'])

        if session.total_size > max_bytes:
            shutil.rmtree(tmp, ignore_errors=True)
            session.status = 'aborted'
            session.save(update_fields=['status', 'updated_at'])
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'FILE_TOO_LARGE',
                        'message': f'Final file would exceed {max_bytes} bytes.',
                        'details': {},
                    },
                },
                status=drf_status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )

        return Response(
            {
                'success': True,
                'fileId': str(session.file_id),
                'chunkIndex': chunk_index,
                'received': received,
                'total': session.total_chunks,
                'bytesReceived': session.total_size,
                'complete': len(received) >= session.total_chunks,
            },
            status=drf_status.HTTP_202_ACCEPTED,
        )

    def _single_shot(self, file_obj, max_bytes):
        if file_obj.size > max_bytes:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'FILE_TOO_LARGE',
                        'message': f'File exceeds {max_bytes} bytes.',
                        'details': {},
                    },
                },
                status=drf_status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            )

        ext = os.path.splitext(file_obj.name)[1]
        target_dir = _final_dir()
        final_name = f'{uuid.uuid4().hex}{ext}'
        dest = os.path.join(target_dir, final_name)
        with open(dest, 'wb') as f:
            for piece in file_obj.chunks():
                f.write(piece)

        import mimetypes
        from django.urls import reverse
        media_url = settings.MEDIA_URL + getattr(settings, 'UPLOAD_FINAL_SUBDIR', 'uploads')
        media_url += f'/{datetime.now(timezone.utc).year:04d}/{datetime.now(timezone.utc).month:02d}/{final_name}'

        item = MediaItem.objects.create(
            file_url=request.build_absolute_uri(media_url),
            filename=file_obj.name,
            file_size=file_obj.size,
            width=0,
            height=0,
            category='image',
            status='Published',
        )

        return Response(
            {
                'success': True,
                'url': item.file_url,
                'fileName': file_obj.name,
                'size': file_obj.size,
                'mimeType': file_obj.content_type or mimetypes.guess_type(file_obj.name)[0] or 'application/octet-stream',
                'id': str(item.id),
            },
            status=drf_status.HTTP_201_CREATED,
        )


class ChunkedUploadCompleteView(APIView):
    """POST /api/uploads/complete

    Body: { fileId, category?, alt?, altAr?, caption?, captionAr? }

    Assembles the chunks, moves them to MEDIA_ROOT/uploads/yyyy/mm/, creates a
    MediaItem, and marks the session completed.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        file_id = request.data.get('fileId') or request.data.get('file_id')
        if not file_id:
            return Response(
                {'success': False, 'error': {'code': 'FILE_ID_REQUIRED', 'message': '`fileId` is required.'}},
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        try:
            session = UploadSession.objects.get(file_id=file_id)
        except (UploadSession.DoesNotExist, ValueError):
            return Response(
                {'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Upload session not found.'}},
                status=drf_status.HTTP_404_NOT_FOUND,
            )

        if session.status == 'completed':
            item = MediaItem.objects.filter(pk=session.media_item_id).first()
            if item:
                return self._ok(item)

        tmp = _tmp_dir(session.file_id)
        expected = set(range(session.total_chunks))
        present = set(session.received_chunks or [])
        missing = sorted(expected - present)
        if missing:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'CHUNKS_MISSING',
                        'message': f'Missing chunks: {missing}',
                        'details': {'missing': missing},
                    },
                },
                status=drf_status.HTTP_409_CONFLICT,
            )

        if not os.path.isdir(tmp):
            return Response(
                {'success': False, 'error': {'code': 'TMP_MISSING', 'message': 'Temporary directory vanished.'}},
                status=drf_status.HTTP_410_GONE,
            )

        ext = os.path.splitext(session.filename)[1]
        target_dir = _final_dir()
        final_name = f'{uuid.uuid4().hex}{ext}'
        final_path = os.path.join(target_dir, final_name)

        with open(final_path, 'wb') as out:
            for idx in range(session.total_chunks):
                chunk_path = os.path.join(tmp, f'{idx:06d}.part')
                with open(chunk_path, 'rb') as in_f:
                    shutil.copyfileobj(in_f, out)

        shutil.rmtree(tmp, ignore_errors=True)

        media_url = (
            settings.MEDIA_URL
            + getattr(settings, 'UPLOAD_FINAL_SUBDIR', 'uploads')
            + f'/{datetime.now(timezone.utc).year:04d}/{datetime.now(timezone.utc).month:02d}/{final_name}'
        )
        absolute = request.build_absolute_uri(media_url)

        category = (request.data.get('category') or 'image').lower()
        if category not in {'image', 'video', 'document'}:
            category = 'image'

        with transaction.atomic():
            item = MediaItem.objects.create(
                file_url=absolute,
                filename=session.filename,
                alt=(request.data.get('alt') or '')[:300],
                alt_ar=(request.data.get('altAr') or '')[:300],
                caption=(request.data.get('caption') or '')[:500],
                caption_ar=(request.data.get('captionAr') or '')[:500],
                file_size=session.total_size or 0,
                width=0,
                height=0,
                category=category,
                status='Published',
            )
            session.status = 'completed'
            session.media_item_id = item.pk
            session.save(update_fields=['status', 'media_item_id', 'updated_at'])

        return self._ok(item)

    def _ok(self, item):
        import mimetypes
        return Response(
            {
                'success': True,
                'url': item.file_url,
                'fileName': item.filename,
                'size': item.file_size,
                'mimeType': mimetypes.guess_type(item.filename)[0] or 'application/octet-stream',
                'id': str(item.id),
                'category': item.category,
            },
            status=drf_status.HTTP_201_CREATED,
        )


class ChunkedUploadAbortView(APIView):
    """POST /api/uploads/abort  body: { fileId }"""

    permission_classes = [AllowAny]

    def post(self, request):
        file_id = request.data.get('fileId') or request.data.get('file_id')
        if not file_id:
            return Response(
                {'success': False, 'error': {'code': 'FILE_ID_REQUIRED', 'message': '`fileId` is required.'}},
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        try:
            session = UploadSession.objects.get(file_id=file_id)
        except (UploadSession.DoesNotExist, ValueError):
            return Response({'success': True, 'message': 'Already gone.'})

        shutil.rmtree(_tmp_dir(session.file_id), ignore_errors=True)
        session.status = 'aborted'
        session.save(update_fields=['status', 'updated_at'])
        return Response({'success': True})
