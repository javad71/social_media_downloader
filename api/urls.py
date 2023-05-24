from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("linkedin/", views.process_linkedin, name="linkedin"),
    path("instagram/", views.process_instagram, name="instagram"),
    path("twitter/", views.process_twitter, name="twitter"),
    path("tiktok/", views.process_tiktok, name="linkedin"),
    path("youtube/", views.process_youtube, name="youtube")
]
