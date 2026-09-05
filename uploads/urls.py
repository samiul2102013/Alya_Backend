from django.urls import path

from .views import ChunkedUploadView, ChunkedUploadCompleteView, ChunkedUploadAbortView

urlpatterns = [
    # Legacy single-shot endpoint + new chunked endpoint (same URL).
    path('uploads', ChunkedUploadView.as_view(), name='file-upload'),
    path('uploads/complete', ChunkedUploadCompleteView.as_view(), name='file-upload-complete'),
    path('uploads/abort', ChunkedUploadAbortView.as_view(), name='file-upload-abort'),
]
