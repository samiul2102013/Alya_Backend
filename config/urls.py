from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import FileResponse, Http404
from django.urls import include, path

from accounts.views import PublicPrivacyPolicyView, PublicTermsView

from config.views import apple_pay_domain_association

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/admin/', include('accounts.urls')),
    path('api/privacy/', PublicPrivacyPolicyView.as_view(), name='privacy-policy'),
    path('api/terms/', PublicTermsView.as_view(), name='terms'),
    path('api/', include('engagement.urls')),
    path('api/', include('content.urls')),
    path('api/', include('uploads.urls')),
    path('api/', include('payments.urls')),
    path('.well-known/apple-developer-merchantid-domain-association', apple_pay_domain_association, name='apple-pay-domain-association'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)