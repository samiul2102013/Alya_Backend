from django.db import connection
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(View):
    """Container & infrastructure health check.

    Implemented as a lightweight standard Django View returning JsonResponse to
    bypass DRF middleware, authentication, and throttling. Docker container
    healthchecks ping this endpoint every 15 seconds; DRF throttling must never
    intercept or rate-limit these pings (which causes false-positive container
    unhealthy errors and deployment failures).
    """

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            return JsonResponse({'status': 'healthy'}, status=200)
        except Exception as e:
            return JsonResponse(
                {'status': 'unhealthy', 'error': str(e)},
                status=503,
            )