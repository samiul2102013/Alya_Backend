from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import AdminUser
from engagement.models import Booking, ContactMessage, InitiativeApplication
from .enums import (
    ApplicationStatus,
    BookingStatus,
    Emirates,
Language,
    MaritalStage,
    ResourceType,
    SessionType,
    ShortCategory,
    Source,
    Status,
    SupportProgram,
)
from .models import Category, Consultation, Emirate, Initiative, NewsArticle, Short


class DashboardStatsView(APIView):
    """/api/admin/dashboard/stats"""

    def get(self, request):
        stats = [
            {'id': 'shorts', 'label': 'Short Videos', 'value': Short.objects.count(), 'icon': 'shorts'},
            {'id': 'initiatives', 'label': 'Initiatives', 'value': Initiative.objects.count(), 'icon': 'initiative'},
            {'id': 'news', 'label': 'News Articles', 'value': NewsArticle.objects.count(), 'icon': 'news'},
            {'id': 'consultations', 'label': 'Active Consultations', 'value': Consultation.objects.filter(status='Published').count(), 'icon': 'consultation'},
            {'id': 'emirates', 'label': 'Total Emirates', 'value': Emirate.objects.count(), 'icon': 'emirates'},
            {'id': 'users', 'label': 'Registered Users', 'value': AdminUser.objects.count(), 'icon': 'users'},
        ]
        return Response(stats)


class DashboardAnalyticsView(APIView):
    """/api/admin/dashboard/analytics"""

    def get(self, request):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        data = [{'month': m, 'revenue': 0, 'users': 0} for m in months]
        return Response(data)


class DashboardLatestContentView(APIView):
    """/api/admin/dashboard/latest-content"""

    def get(self, request):
        items = []
        for short in Short.objects.all().order_by('-created_at')[:5]:
            items.append({
                'id': str(short.pk),
                'title': short.video_title,
                'contentType': 'short',
                'module': 'Shorts',
                'dateTime': short.created_at,
                'status': short.status,
            })
        for news in NewsArticle.objects.all().order_by('-created_at')[:5]:
            items.append({
                'id': str(news.pk),
                'title': news.article_title,
                'contentType': 'news',
                'module': 'News',
                'dateTime': news.created_at,
                'status': news.status,
            })
        for initiative in Initiative.objects.all().order_by('-created_at')[:5]:
            items.append({
                'id': str(initiative.pk),
                'title': initiative.title,
                'contentType': 'initiative',
                'module': 'Initiatives',
                'dateTime': initiative.created_at,
                'status': initiative.status,
            })
        for consultation in Consultation.objects.all().order_by('-created_at')[:5]:
            items.append({
                'id': str(consultation.pk),
                'title': consultation.session_title,
                'contentType': 'consultation',
                'module': 'Consultations',
                'dateTime': consultation.created_at,
                'status': consultation.status,
            })
        items.sort(key=lambda item: item['dateTime'], reverse=True)
        return Response(items[:5])


class MetaView(APIView):
    """/api/admin/meta"""

    def get(self, request):
        return Response({
            'emirates': [{'value': choice.value, 'label': choice.label} for choice in Emirates],
            'categories': [name for name in ShortCategory.values],
            'languages': [{'value': choice.value, 'label': choice.label} for choice in Language],
            'emblems': [{'value': choice.value, 'label': choice.label} for choice in Emirates],
            'sessionTypes': [{'value': choice.value, 'label': choice.label} for choice in SessionType],
            'maritalStages': [{'value': choice.value, 'label': choice.label} for choice in MaritalStage],
            'sources': [{'value': choice.value, 'label': choice.label} for choice in Source],
            'resourceTypes': [{'value': choice.value, 'label': choice.label} for choice in ResourceType],
            'supportPrograms': [{'value': choice.value, 'label': choice.label} for choice in SupportProgram],
            'bookingStatuses': [{'value': choice.value, 'label': choice.label} for choice in BookingStatus],
            'applicationStatuses': [{'value': choice.value, 'label': choice.label} for choice in ApplicationStatus],
            'statuses': [{'value': choice.value, 'label': choice.label} for choice in Status],
        })