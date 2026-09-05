from django.db import models
import uuid


class UploadSession(models.Model):
    """Server-side state for a single in-progress chunked upload.

    The frontend slices a file into chunks and POSTs each chunk (with the same
    `file_id`) to /api/uploads. When all chunks are received the client calls
    /api/uploads/complete, which assembles the file, creates a MediaItem, and
    marks the session completed.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('aborted', 'Aborted'),
    ]

    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=500)
    mime_type = models.CharField(max_length=120, blank=True)
    total_chunks = models.PositiveIntegerField()
    received_chunks = models.JSONField(default=list, blank=True,
        help_text='List of chunk indexes that have been uploaded (e.g. [0,1,2]).')
    total_size = models.PositiveBigIntegerField(default=0,
        help_text='Sum of all chunk byte sizes; checked against MAX_UPLOAD_SIZE_BYTES on completion.')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    media_item_id = models.UUIDField(null=True, blank=True,
        help_text='Set after completion: the MediaItem pk that owns the assembled file.')
    uploaded_by = models.CharField(max_length=200, blank=True,
        help_text='AdminUser identifier (email) for auditing.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Upload Session'
        verbose_name_plural = 'Upload Sessions'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.filename} ({self.status})'
