import logging
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound

logger = logging.getLogger(__name__)


def apple_pay_domain_association(request):
    """Serve the Apple Pay domain verification file.

    Many payment processors (Stripe included) host this file for you after you
    register the domain in their dashboard. If a static copy is supplied at
    ``APPLE_PAY_DOMAIN_ASSOCIATION_FILE`` it is served here as a fallback /
    when self-hosting the association.
    """
    configured = getattr(settings, 'APPLE_PAY_DOMAIN_ASSOCIATION_FILE', '') or ''
    if configured:
        path = Path(configured)
        if path.is_file():
            return HttpResponse(path.read_bytes(), content_type='text/plain')

    logger.error(
        'Apple Pay domain association file is not configured. Set '
        'APPLE_PAY_DOMAIN_ASSOCIATION_FILE (and complete Apple Pay setup / domain '
        'registration on the payment processor) for Apple Pay to appear.'
    )
    return HttpResponseNotFound('Not found')
