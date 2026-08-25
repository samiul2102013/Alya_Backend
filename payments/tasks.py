from celery import shared_task

from payments import services


@shared_task(name='payments.tasks.release_expired_pending_bookings')
def release_expired_pending_bookings():
    """Periodic seat-release job: cancel pending bookings past their expiry."""
    return services.release_expired_bookings()
