import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Convert DRF exceptions into the contract error envelope.

    {
      "success": false,
      "error": { "code": "...", "message": "...", "details": { field: [...] } }
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data

        code = getattr(exc, 'default_code', 'error')
        message = 'Request failed'
        detail = {}

        if isinstance(data, dict):
            message = data.get('message') or data.get('detail') or message
            detail = data.get('details') or {}
            if not detail:
                field_errors = {
                    k: v for k, v in data.items()
                    if k not in ('detail', 'message', 'code')
                }
                if field_errors:
                    detail = field_errors
        else:
            message = str(data)

        if code == 'validation_error':
            code = 'VALIDATION_ERROR'
        elif code == 'not_found':
            code = 'NOT_FOUND'
        elif code == 'not_authenticated':
            code = 'UNAUTHORIZED'
        elif code == 'permission_denied':
            code = 'FORBIDDEN'
        elif code == 'authentication_failed':
            code = 'UNAUTHORIZED'
        else:
            code = code.upper().replace('-', '_').replace(' ', '_')

        envelope = {
            'success': False,
            'error': {'code': code, 'message': message, 'details': detail},
        }
        logger.error(
            'API Error [%s] %s', code, message,
            extra={'exception': repr(exc)},
        )
        return Response(envelope, status=response.status_code)

    logger.error('Unhandled API Error', exc_info=True)
    return Response(
        {
            'success': False,
            'error': {
                'code': 'SERVER_ERROR',
                'message': 'An unexpected error occurred',
                'details': {},
            },
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )