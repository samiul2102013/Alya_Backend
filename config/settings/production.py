from .base import *

DEBUG = False
ALLOWED_HOSTS = list(set(env.list('ALLOWED_HOSTS', default=['api.wileef.com', 'localhost', '127.0.0.1']) + ['localhost', '127.0.0.1', '0.0.0.0', 'testserver']))

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

# The app is served behind nginx -> Traefik/Cloudflare. Trust the proxy headers so
# request.is_secure(), secure cookies, and the CSRF origin check all see HTTPS.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# TLS is terminated at the Traefik edge (nginx reaches gunicorn over plain HTTP), so
# Django must NOT attempt an SSL redirect. Redirecting here would turn every request
# (including the container healthcheck) into an endless https:// -> connection failure.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False},
        'celery': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False},
    },
}