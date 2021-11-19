from django.urls import path
from streamapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sensors", views.sensors, name="sensors"),
    path("video_feed", views.video_feed, name="video_feed"),
    path("plants", views.plants, name="plants"),
    path("control", views.control, name="control"),
    path("settings", views.settings, name="settings"),
]
