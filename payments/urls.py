from django.urls import path

from .views import CreatePaymentIntentView, stripe_webhook

app_name = 'payments'

urlpatterns = [
    path('payments/create-intent', CreatePaymentIntentView.as_view(), name='payments-create-intent'),
    path('payments/webhook', stripe_webhook, name='payments-webhook'),
]
