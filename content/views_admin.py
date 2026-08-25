from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .admin_serializers import (
    CategoryAdminSerializer,
    ConsultationAdminSerializer,
    EmirateAdminSerializer,
    InitiativeAdminSerializer,
    NewsAdminSerializer,
    PagePresentationAdminSerializer,
    ShortAdminSerializer,
)
from .models import (
    Category,
    Consultation,
    Emirate,
    Initiative,
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