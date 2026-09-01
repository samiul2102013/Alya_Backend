import mimetypes
import os
import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class FileUploadView(APIView):
    """POST /api/uploads — multipart/form-data with `file` field.

    Returns: { url, fileName, size, mimeType }
    """

    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response(
                {
                    'success': False,
                    'error': {
                        'code': 'FILE_REQUIRED',
                        'message': 'A file is required',
                        'details': {'file': ['This field is required']},
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ext = os.path.splitext(file_obj.name)[1]
        filename = f'{uuid.uuid4().hex}{ext}'
        subdir = getattr(settings, 'UPLOAD_SUBDIR', 'uploads')
        upload_root = os.path.join(settings.MEDIA_ROOT, subdir)
        os.makedirs(upload_root, exist_ok=True)
        dest = os.path.join(upload_root, filename)

        with open(dest, 'wb') as f:
            for chunk in file_obj.chunks(chunk_size=1024 * 1024 * 10):
                f.write(chunk)

        media_url = f'{settings.MEDIA_URL}{subdir}/{filename}'
        absolute = request.build_absolute_uri(media_url)

        return Response(
            {
                'url': absolute,
                'fileName': file_obj.name,
                'size': file_obj.size,
                'mimeType': file_obj.content_type or mimetypes.guess_type(file_obj.name)[0] or 'application/octet-stream',
            },
            status=status.HTTP_201_CREATED,
        )