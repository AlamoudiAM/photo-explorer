from django.urls import path
from . import views

urlpatterns = [
    path('view-video/<encrypted_file_fullpath>', views.view_video, name='media'),
    path('get-video/<m3u8_request_identifier>/<ts_filename>', views.get_video, name='media'),
]
