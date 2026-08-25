from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Category, Consultation, Emirate, Initiative, NewsArticle, PagePresentation, Short
from .public_serializers import (
    CategorySerializer,
    ConsultationDetailSerializer,
    ConsultationListSerializer,
    EmirateDetailSerializer,
    EmirateListSerializer,
    InitiativeDetailSerializer,
    InitiativeListSerializer,
    NewsDetailSerializer,
    NewsListSerializer,
    PagePresentationSerializer,
    ShortDetailSerializer,
    ShortListSerializer,
)


class ShortPublicView(generics.ListAPIView):
    """GET /api/shorts — published videos only.

    Paginated ({data, meta}) by default. Supports `page` and `perPage` query params.
    Optional query params: search, marital_stage, language, date (week|month|year).
    """

    permission_classes = [AllowAny]
    serializer_class = ShortListSerializer

    def get_queryset(self):
        params = self.request.query_params
        qs = Short.objects.filter(status='Published')

        search = params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(video_title__icontains=search)
                | Q(video_title_ar__icontains=search)
            )

        marital_stage = params.get('marital_stage', '').strip()
        if marital_stage in ('premarital', 'marital', 'postMarital'):
            qs = qs.filter(marital_stage=marital_stage)

        language = params.get('language', '').strip()
        if language in ('ar', 'en', 'both'):
            qs = qs.filter(language=language)

        date = params.get('date', '').strip()
        if date in ('week', 'month', 'year'):
            now = timezone.now()
            if date == 'week':
                qs = qs.filter(published_at__gte=now - timedelta(weeks=1))
            elif date == 'month':
                qs = qs.filter(published_at__gte=now - timedelta(days=30))
            else:
                qs = qs.filter(published_at__gte=now - timedelta(days=365))

        return qs.order_by('-published_at')


class ShortPublicDetail(generics.RetrieveAPIView):
    """GET /api/shorts/:slug/"""

    permission_classes = [AllowAny]
    serializer_class = ShortDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Short.objects.filter(status='Published')


class NewsPublicList(generics.ListAPIView):
    """GET /api/news/ — published articles only.

    Optional query params: search, category, source, date (week|month|year),
    plus standard pagination (page, perPage).
    """

    permission_classes = [AllowAny]
    serializer_class = NewsListSerializer

    def get_queryset(self):
        params = self.request.query_params
        qs = NewsArticle.objects.filter(status='Published')

        search = params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(article_title__icontains=search)
                | Q(article_title_ar__icontains=search)
                | Q(content__icontains=search)
                | Q(organization__icontains=search)
            )

        category = params.get('category', '').strip()
        if category:
            qs = qs.filter(category__iexact=category)

        source = params.get('source', '').strip()
        if source:
            qs = qs.filter(source__iexact=source)

        date = params.get('date', '').strip()
        if date in ('week', 'month', 'year'):
            today = timezone.now().date()
            if date == 'week':
                qs = qs.filter(published_date__gte=today - timedelta(weeks=1))
            elif date == 'month':
                qs = qs.filter(published_date__gte=today - timedelta(days=30))
            else:
                qs = qs.filter(published_date__gte=today - timedelta(days=365))

        return qs.order_by('-published_date', '-created_at')


class NewsPublicDetailView(generics.RetrieveAPIView):
    """GET /api/news/:slug/"""

    permission_classes = [AllowAny]
    serializer_class = NewsDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return NewsArticle.objects.filter(status='Published')


class InitiativePublicList(generics.ListAPIView):
    """GET /api/initiatives/

    Optional query params: emirate, featured (1/0).
    """

    permission_classes = [AllowAny]
    serializer_class = InitiativeListSerializer

    def get_queryset(self):
        qs = Initiative.objects.filter(status='Published')
        emirate = self.request.query_params.get('emirate')
        featured = self.request.query_params.get('featured')
        if emirate:
            qs = qs.filter(emirates__iexact=emirate)
        if featured == '1':
            qs = qs.filter(is_featured=True)
        elif featured == '0':
            qs = qs.filter(is_featured=False)
        return qs


class InitiativeFeaturedPublicView(generics.RetrieveAPIView):
    """GET /api/initiatives/featured — returns the single featured initiative (or 404)."""

    permission_classes = [AllowAny]
    serializer_class = InitiativeDetailSerializer

    def get_object(self):
        obj = Initiative.objects.filter(status='Published', is_featured=True).first()
        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound('No featured initiative found.')
        return obj


class InitiativePublicDetailView(generics.RetrieveAPIView):
    """GET /api/initiatives/:slug/"""

    permission_classes = [AllowAny]
    serializer_class = InitiativeDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Initiative.objects.filter(status='Published')


class ConsultationPublicList(generics.ListAPIView):
    """GET /api/consultations/ — published sessions only.

    Optional query params: search, marital_stage, language, date (week|month|year),
    free (true|1), emirate.
    """

    permission_classes = [AllowAny]
    serializer_class = ConsultationListSerializer

    def get_queryset(self):
        params = self.request.query_params
        qs = Consultation.objects.filter(status='Published')

        search = params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(session_title__icontains=search) | Q(session_title_ar__icontains=search)
            )

        marital_stage = params.get('marital_stage', '').strip()
        if marital_stage in ('premarital', 'marital', 'postMarital'):
            qs = qs.filter(marital_stage=marital_stage)

        language = params.get('language', '').strip()
        if language in ('ar', 'en', 'both'):
            qs = qs.filter(language=language)

        free = params.get('free', '').strip().lower()
        if free in ('true', '1'):
            qs = qs.filter(is_free=True)
        elif free in ('false', '0'):
            qs = qs.filter(is_free=False)

        emirate = params.get('emirate', '').strip()
        if emirate:
            qs = qs.filter(emirates__iexact=emirate)

        date = params.get('date', '').strip()
        if date in ('week', 'month', 'year'):
            now = timezone.now().date()
            if date == 'week':
                qs = qs.filter(date__gte=now - timedelta(weeks=1))
            elif date == 'month':
                qs = qs.filter(date__gte=now - timedelta(days=30))
            else:
                qs = qs.filter(date__gte=now - timedelta(days=365))

        return qs.order_by('-date', '-created_at')


class ConsultationPublicDetailView(generics.RetrieveAPIView):
    """GET /api/consultations/:slug/"""

    permission_classes = [AllowAny]
    serializer_class = ConsultationDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Consultation.objects.filter(status='Published')


class EmiratePublicList(generics.ListAPIView):
    """GET /api/emirates/"""

    permission_classes = [AllowAny]
    serializer_class = EmirateListSerializer

    def get_queryset(self):
        return Emirate.objects.filter(status='Published')


class EmiratePublicDetailView(generics.RetrieveAPIView):
    """GET /api/emirates/:slug/"""

    permission_classes = [AllowAny]
    serializer_class = EmirateDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Emirate.objects.filter(status='Published')


class CategoryPublicList(generics.ListAPIView):
    """GET /api/categories/"""

    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(status='Published')


class ConsultationPublicDetailByNameView(generics.RetrieveAPIView):
    """GET /api/consultations/:sessionTitle/ (name lookup fallback)"""

    permission_classes = [AllowAny]
    serializer_class = ConsultationDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get(self.lookup_field)
        if not slug:
            return None
        obj = Consultation.objects.filter(slug=slug, status='Published').first()
        if not obj:
            obj = Consultation.objects.filter(session_title__iexact=slug, status='Published').first()
        if not obj:
            self.permission_denied(self.request)
        return obj


class PagePresentationPublicListView(generics.ListAPIView):
    """GET /api/presentations — all published page presentations."""

    permission_classes = [AllowAny]
    serializer_class = PagePresentationSerializer
    pagination_class = None

    def get_queryset(self):
        return PagePresentation.objects.filter(published=True)


class PagePresentationPublicDetailView(generics.RetrieveAPIView):
    """GET /api/presentations/:key/ — a single published page presentation."""

    permission_classes = [AllowAny]
    serializer_class = PagePresentationSerializer
    lookup_field = 'key'

    def get_queryset(self):
        return PagePresentation.objects.filter(published=True)
