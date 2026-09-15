from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .admin_serializers import (
    AboutContentAdminSerializer,
    CategoryAdminSerializer,
    ConsultationAdminSerializer,
    ContactContentAdminSerializer,
    EmirateAdminSerializer,
    FooterContentAdminSerializer,
    HomepageContentAdminSerializer,
    InitiativeAdminSerializer,
    MediaItemAdminSerializer,
    NewsAdminSerializer,
    PagePresentationAdminSerializer,
    ShortAdminSerializer,
)
from .models import (
    AboutContent,
    Category,
    Consultation,
    ContactContent,
    Emirate,
    FooterContent,
    HomepageContent,
    Initiative,
    MediaItem,
    NewsArticle,
    PagePresentation,
    Short,
)


class ShortAdminViewSet(ModelViewSet):
    """/api/admin/shorts"""

    queryset = Short.objects.all().order_by('-created_at')
    serializer_class = ShortAdminSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        status_filter = self.request.query_params.get('status')
        if search:
            qs = qs.filter(
                Q(video_title__icontains=search) | Q(organization__icontains=search)
            )
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        return qs


class NewsAdminViewSet(ModelViewSet):
    """/api/admin/news"""

    queryset = NewsArticle.objects.all().order_by('-created_at')
    serializer_class = NewsAdminSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        status_filter = self.request.query_params.get('status')
        if search:
            qs = qs.filter(
                Q(article_title__icontains=search) | Q(organization__icontains=search)
            )
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        return qs


class InitiativeAdminViewSet(ModelViewSet):
    """/api/admin/initiatives"""

    queryset = Initiative.objects.all().order_by('-created_at')
    serializer_class = InitiativeAdminSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        status_filter = self.request.query_params.get('status')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(subtitle__icontains=search))
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        return qs


class ConsultationAdminViewSet(ModelViewSet):
    """/api/admin/consultations"""

    queryset = Consultation.objects.all().order_by('-created_at')
    serializer_class = ConsultationAdminSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        status_filter = self.request.query_params.get('status')
        if search:
            qs = qs.filter(Q(session_title__icontains=search) | Q(counselor__icontains=search))
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        return qs


class EmirateAdminViewSet(ModelViewSet):
    """/api/admin/emirates"""

    queryset = Emirate.objects.all().order_by('emirates_name')
    serializer_class = EmirateAdminSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        status_filter = self.request.query_params.get('status')
        if search:
            qs = qs.filter(emirates_name__icontains=search)
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        return qs


class CategoryAdminViewSet(ModelViewSet):
    """/api/admin/categories"""

    queryset = Category.objects.all().order_by('name')
    serializer_class = CategoryAdminSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class PagePresentationAdminViewSet(ModelViewSet):
    """/api/admin/presentations"""

    queryset = PagePresentation.objects.all().order_by('key')
    serializer_class = PagePresentationAdminSerializer
    lookup_field = 'pk'


class HomepageContentAdminView(APIView):
    """/api/admin/homepage — upsert singleton homepage content."""

    def get(self, request):
        obj, _ = HomepageContent.objects.get_or_create(pk=HomepageContent.objects.first().pk if HomepageContent.objects.exists() else None)
        serializer = HomepageContentAdminSerializer(obj)
        return Response(serializer.data)

    def post(self, request):
        obj = HomepageContent.objects.first()
        if obj:
            serializer = HomepageContentAdminSerializer(obj, data=request.data, partial=True)
        else:
            serializer = HomepageContentAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AboutContentAdminView(APIView):
    """/api/admin/about — upsert singleton about content."""

    def get(self, request):
        obj, _ = AboutContent.objects.get_or_create(pk=AboutContent.objects.first().pk if AboutContent.objects.exists() else None)
        serializer = AboutContentAdminSerializer(obj)
        return Response(serializer.data)

    def post(self, request):
        obj = AboutContent.objects.first()
        if obj:
            serializer = AboutContentAdminSerializer(obj, data=request.data, partial=True)
        else:
            serializer = AboutContentAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactContentAdminView(APIView):
    """/api/admin/contact — upsert singleton contact content."""

    def get(self, request):
        obj, _ = ContactContent.objects.get_or_create(pk=ContactContent.objects.first().pk if ContactContent.objects.exists() else None)
        serializer = ContactContentAdminSerializer(obj)
        return Response(serializer.data)

    def post(self, request):
        obj = ContactContent.objects.first()
        if obj:
            serializer = ContactContentAdminSerializer(obj, data=request.data, partial=True)
        else:
            serializer = ContactContentAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FooterContentAdminView(APIView):
    """/api/admin/footer — upsert singleton footer content."""

    def get(self, request):
        # Always return the full pre-filled footer so the admin panel shows
        # exactly what the user panel renders, even before the first save.
        obj = FooterContent.get_or_load()
        serializer = FooterContentAdminSerializer(obj)
        return Response(serializer.data)

    def post(self, request):
        obj = FooterContent.objects.first()
        if obj:
            serializer = FooterContentAdminSerializer(obj, data=request.data, partial=True)
        else:
            serializer = FooterContentAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MediaItemAdminViewSet(ModelViewSet):
    """/api/admin/media"""

    queryset = MediaItem.objects.all().order_by('-created_at')
    serializer_class = MediaItemAdminSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        status_filter = self.request.query_params.get('status')
        category_filter = self.request.query_params.get('category')
        if search:
            qs = qs.filter(Q(filename__icontains=search) | Q(alt__icontains=search))
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        if category_filter:
            qs = qs.filter(category__iexact=category_filter)
        return qs


class RetranslateAdminView(APIView):
    """POST /api/admin/retranslate — (re)generate machine Arabic for a record.

    Body: { "model": "short"|"news"|"initiative"|"consultation"|"emirate"|
            "category"|"presentation"|"homepage"|"about"|"contact"|"footer",
            "id": "<uuid>",
            "force": bool   (regenerate machine Arabic),
            "force_human": bool (also overwrite human-reviewed Arabic) }

    Safety rules:
    - Human-reviewed Arabic is NEVER touched unless force_human=true is sent
      explicitly.
    - Failed provider calls are not persisted; a retry can be run again later.
    """

    MODEL_MAP = {
        'short': Short,
        'news': NewsArticle,
        'initiative': Initiative,
        'consultation': Consultation,
        'emirate': Emirate,
        'category': Category,
        'presentation': PagePresentation,
        'homepage': HomepageContent,
        'about': AboutContent,
        'contact': ContactContent,
        'footer': FooterContent,
    }

    def post(self, request):
        from .translation import retranslate_object, reset_failure_state

        model_key = str(request.data.get('model', '')).strip().lower()
        model = self.MODEL_MAP.get(model_key)
        if model is None:
            return Response(
                {'detail': f"Unknown model '{model_key}'. Valid: {sorted(self.MODEL_MAP)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        record_id = request.data.get('id')
        instance = model.objects.filter(pk=record_id).first() if record_id else model.objects.first()
        if instance is None:
            return Response(
                {'detail': 'Record not found. Provide a valid "id" (or none for the singleton).'},
                status=status.HTTP_404_NOT_FOUND,
            )

        force = bool(request.data.get('force', False))
        force_human = bool(request.data.get('force_human', False))
        # A deliberate retry must reach the provider even if it failed recently.
        reset_failure_state()
        results = retranslate_object(instance, force=force, force_human=force_human)
        return Response({
            'model': model_key,
            'id': str(instance.pk),
            'force': force,
            'force_human': force_human,
            'updated_fields': results,
        })