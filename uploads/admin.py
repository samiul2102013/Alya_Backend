from django.contrib import admin

from .models import UploadSession


@admin.register(UploadSession)
class UploadSessionAdmin(admin.ModelAdmin):
    list_display = ('filename', 'status', 'total_chunks', 'total_size', 'created_at')
    list_filter = ('status',)
    search_fields = ('filename',)
    readonly_fields = ('file_id', 'received_chunks', 'total_size', 'created_at', 'updated_at', 'media_item_id')
