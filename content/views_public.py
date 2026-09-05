from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AboutContent, Category, Consultation, ContactContent, Emirate, HomepageContent, Initiative, MediaItem, NewsArticle, PagePresentation, Short
from .public_serializers import (
    AboutContentSerializer,
    CategorySerializer,
    ConsultationDetailSerializer,
    ConsultationListSerializer,
    ContactContentSerializer,
    EmirateDetailSerializer,
    EmirateListSerializer,
    HomepageContentSerializer,
    InitiativeDetailSerializer,
    InitiativeListSerializer,
    MediaItemListSerializer,
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

    Optional query params: emirate, featured (1/0), listed (1/0), category, search.
    """

    permission_classes = [AllowAny]
    serializer_class = InitiativeListSerializer

    def get_queryset(self):
        qs = Initiative.objects.filter(status='Published')
        params = self.request.query_params
        emirate = params.get('emirate')
        featured = params.get('featured')
        listed = params.get('listed')
        category = params.get('category', '').strip()
        search = params.get('search', '').strip()

        if emirate:
            qs = qs.filter(emirates__iexact=emirate)
        if featured == '1':
            qs = qs.filter(is_featured=True)
        elif featured == '0':
            qs = qs.filter(is_featured=False)
        if listed == '1':
            qs = qs.filter(is_listed=True)
        elif listed == '0':
            qs = qs.filter(is_listed=False)
        if category:
            qs = qs.filter(category__iexact=category)
        if search:
            qs = qs.filter(
                Q(title__icontains=search)
                | Q(title_ar__icontains=search)
                | Q(subtitle__icontains=search)
                | Q(subtitle_ar__icontains=search)
                | Q(description__icontains=search)
                | Q(purpose__icontains=search)
            )
        return qs.order_by('-is_featured', '-start_date', '-created_at')


class InitiativeFeaturedPublicView(generics.RetrieveAPIView):
    """GET /api/initiatives/featured — returns the single featured initiative (or 404)."""

    permission_classes = [AllowAny]
    serializer_class = InitiativeDetailSerializer

    def get_object(self):
        obj = Initiative.objects.filter(status='Published', is_featured=True).first()
        if not obj:
            obj = Initiative.objects.filter(status='Published').first()
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
    """GET /api/emirates/ — published emirates only.

    Optional query params: search, date (week|month|year).
    """

    permission_classes = [AllowAny]
    serializer_class = EmirateListSerializer

    def get_queryset(self):
        params = self.request.query_params
        qs = Emirate.objects.filter(status='Published')

        search = params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(emirates_name__icontains=search)
                | Q(emirates_name_ar__icontains=search)
                | Q(title__icontains=search)
                | Q(description__icontains=search)
            )

        date = params.get('date', '').strip()
        if date in ('week', 'month', 'year'):
            now = timezone.now()
            if date == 'week':
                qs = qs.filter(date_time__gte=now - timedelta(weeks=1))
            elif date == 'month':
                qs = qs.filter(date_time__gte=now - timedelta(days=30))
            else:
                qs = qs.filter(date_time__gte=now - timedelta(days=365))

        return qs.order_by('-date_time', 'emirates_name')


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


class HomepageContentPublicView(generics.RetrieveAPIView):
    """GET /api/homepage — returns the singleton homepage content."""

    permission_classes = [AllowAny]
    serializer_class = HomepageContentSerializer

    def get_object(self):
        obj = HomepageContent.objects.first()
        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound('Homepage content not configured yet.')
        return obj


class AboutContentPublicView(generics.RetrieveAPIView):
    """GET /api/about — returns the singleton about content."""

    permission_classes = [AllowAny]
    serializer_class = AboutContentSerializer

    def get_object(self):
        obj = AboutContent.objects.first()
        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound('About content not configured yet.')
        return obj


class ContactContentPublicView(generics.RetrieveAPIView):
    """GET /api/contact — returns the singleton contact content."""

    permission_classes = [AllowAny]
    serializer_class = ContactContentSerializer

    def get_object(self):
        obj = ContactContent.objects.first()
        if not obj:
            from rest_framework.exceptions import NotFound
            raise NotFound('Contact content not configured yet.')
        return obj


class MediaItemPublicList(generics.ListAPIView):
    """GET /api/media — published media items."""

    permission_classes = [AllowAny]
    serializer_class = MediaItemListSerializer

    def get_queryset(self):
        params = self.request.query_params
        qs = MediaItem.objects.filter(status='Published')
        category = params.get('category', '').strip()
        if category:
            qs = qs.filter(category__iexact=category)
        return qs.order_by('-created_at')


class GlobalSearchView(APIView):
    """GET /api/search?q=...

    Returns grouped hits across shorts, news, consultations, initiatives, and
    emirates — each limited to a handful of items so the search results page
    stays snappy. All sources are restricted to status='Published'.
    """

    permission_classes = [AllowAny]

    MAX_PER_GROUP = 4

    def get(self, request):
        q = (request.query_params.get('q') or '').strip()
        if not q:
            return Response({
                'q': '',
                'shorts': [],
                'news': [],
                'consultations': [],
                'initiatives': [],
                'emirates': [],
            })

        shorts = Short.objects.filter(status='Published').filter(
            Q(video_title__icontains=q)
            | Q(video_title_ar__icontains=q)
            | Q(description__icontains=q)
            | Q(organization__icontains=q)
        ).order_by('-published_at', '-created_at')[:self.MAX_PER_GROUP]

        news = NewsArticle.objects.filter(status='Published').filter(
            Q(article_title__icontains=q)
            | Q(article_title_ar__icontains=q)
            | Q(content__icontains=q)
            | Q(organization__icontains=q)
        ).order_by('-published_date', '-created_at')[:self.MAX_PER_GROUP]

        consultations = Consultation.objects.filter(status='Published').filter(
            Q(session_title__icontains=q)
            | Q(session_title_ar__icontains=q)
            | Q(counselor__icontains=q)
        ).order_by('-date', '-created_at')[:self.MAX_PER_GROUP]

        initiatives = Initiative.objects.filter(status='Published').filter(
            Q(title__icontains=q)
            | Q(title_ar__icontains=q)
            | Q(subtitle__icontains=q)
            | Q(description__icontains=q)
            | Q(purpose__icontains=q)
        ).order_by('-start_date', '-created_at')[:self.MAX_PER_GROUP]

        emirates = Emirate.objects.filter(status='Published').filter(
            Q(emirates_name__icontains=q)
            | Q(title__icontains=q)
            | Q(description__icontains=q)
        ).order_by('emirates_name')[:self.MAX_PER_GROUP]

        return Response({
            'q': q,
            'shorts': ShortListSerializer(shorts, many=True).data,
            'news': NewsListSerializer(news, many=True).data,
            'consultations': ConsultationListSerializer(consultations, many=True).data,
            'initiatives': InitiativeListSerializer(initiatives, many=True).data,
            'emirates': EmirateListSerializer(emirates, many=True).data,
        })
