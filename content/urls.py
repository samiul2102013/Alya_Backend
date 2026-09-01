from django.urls import path
from rest_framework.routers import DefaultRouter

from .dashboard import (
    DashboardAnalyticsView,
    DashboardLatestContentView,
    DashboardStatsView,
    MetaView,
)
from .views_public import (
    AboutContentPublicView,
    CategoryPublicList,
    ConsultationPublicDetailByNameView,
    ConsultationPublicDetailView,
    ConsultationPublicList,
    ContactContentPublicView,
    EmiratePublicDetailView,
    EmiratePublicList,
    HomepageContentPublicView,
    InitiativeFeaturedPublicView,
    InitiativePublicDetailView,
    InitiativePublicList,
    MediaItemPublicList,
    NewsPublicDetailView,
    NewsPublicList,
    PagePresentationPublicDetailView,
    PagePresentationPublicListView,
    ShortPublicDetail,
    ShortPublicView,
)
from .views_admin import (
    AboutContentAdminView,
    CategoryAdminViewSet,
    ConsultationAdminViewSet,
    ContactContentAdminView,
    EmirateAdminViewSet,
    HomepageContentAdminView,
    InitiativeAdminViewSet,
    MediaItemAdminViewSet,
    NewsAdminViewSet,
    PagePresentationAdminViewSet,
    ShortAdminViewSet,
)

router = DefaultRouter(trailing_slash=False)
router.register(r'admin/shorts', ShortAdminViewSet, basename='admin-shorts')
router.register(r'admin/news', NewsAdminViewSet, basename='admin-news')
router.register(r'admin/initiatives', InitiativeAdminViewSet, basename='admin-initiatives')
router.register(r'admin/consultations', ConsultationAdminViewSet, basename='admin-consultations')
router.register(r'admin/emirates', EmirateAdminViewSet, basename='admin-emirates')
router.register(r'admin/categories', CategoryAdminViewSet, basename='admin-categories')
router.register(r'admin/presentations', PagePresentationAdminViewSet, basename='admin-presentations')
router.register(r'admin/media', MediaItemAdminViewSet, basename='admin-media')

urlpatterns = router.urls + [
    # Dashboard
    path('admin/dashboard/stats', DashboardStatsView.as_view(), name='admin-dashboard-stats'),
    path('admin/dashboard/analytics', DashboardAnalyticsView.as_view(), name='admin-dashboard-analytics'),
    path('admin/dashboard/latest-content', DashboardLatestContentView.as_view(), name='admin-dashboard-latest'),
    path('admin/meta', MetaView.as_view(), name='admin-meta'),
    path('admin/homepage', HomepageContentAdminView.as_view(), name='admin-homepage'),
    path('admin/about', AboutContentAdminView.as_view(), name='admin-about'),
    path('admin/contact', ContactContentAdminView.as_view(), name='admin-contact'),
    # Public
    path('shorts', ShortPublicView.as_view(), name='shorts-list'),
    path('shorts/<str:slug>', ShortPublicDetail.as_view(), name='shorts-detail'),
    path('news', NewsPublicList.as_view(), name='news-list'),
    path('news/<str:slug>', NewsPublicDetailView.as_view(), name='news-detail'),
    path('initiatives/featured', InitiativeFeaturedPublicView.as_view(), name='initiatives-featured'),
    path('initiatives', InitiativePublicList.as_view(), name='initiatives-list'),
    path('initiatives/<str:slug>', InitiativePublicDetailView.as_view(), name='initiatives-detail'),
    path('consultations', ConsultationPublicList.as_view(), name='consultations-list'),
    path('consultations/<str:slug>', ConsultationPublicDetailView.as_view(), name='consultations-detail'),
    path('emirates', EmiratePublicList.as_view(), name='emirates-list'),
    path('emirates/<str:slug>', EmiratePublicDetailView.as_view(), name='emirates-detail'),
    path('categories', CategoryPublicList.as_view(), name='categories-list'),
    path('presentations', PagePresentationPublicListView.as_view(), name='presentations-list'),
    path('presentations/<str:key>', PagePresentationPublicDetailView.as_view(), name='presentations-detail'),
    path('homepage', HomepageContentPublicView.as_view(), name='homepage-content'),
    path('about', AboutContentPublicView.as_view(), name='about-content'),
    path('contact', ContactContentPublicView.as_view(), name='contact-content'),
    path('media', MediaItemPublicList.as_view(), name='media-list'),
]