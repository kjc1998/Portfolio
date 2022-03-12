from django.urls import path
from . import views
from portfolio.settings import ROOT_URL

app_name = "project"

if ROOT_URL:
    urlpatterns = [
        path("", views.projectManagement, name="projectManagement"),
        path("/<int:pid>", views.projectMain, name="projectMain"),
        path("/<int:pid>/<int:sid>", views.storyMain, name="storyMain"),
    ]
else:
    urlpatterns = [
        path("", views.projectManagement, name="projectManagement"),
        path("<int:pid>", views.projectMain, name="projectMain"),
        path("<int:pid>/<int:sid>", views.storyMain, name="storyMain"),
    ]
