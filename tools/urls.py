from django.urls import path
from . import views
urlpatterns=[
    path("add-subtitles/",views.add_subtitles,name="add_subtitles"),
    path("to-audio/",views.to_audio,name="to_audio"),
    path("change-format/",views.change_format,name="change_format"),
    path("extract-frames/",views.extract_frames,name="extract_frames"),
]