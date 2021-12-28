from django.urls import path
from . import views

app_name = "mainFrame"
urlpatterns = [
    path("", views.mainFrame, name="mainFrame"),
    path("<str:name>", views.mainFrame, name="mainFrame")
]
