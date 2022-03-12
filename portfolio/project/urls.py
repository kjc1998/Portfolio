from django.urls import path
from . import views

app_name = "project"

urlpatterns = [
    path("", views.projectManagement, name="projectManagement"),
    path("<int:pid>/", views.projectMain, name="projectMain"),
    path("<int:pid>/<int:sid>/", views.storyMain, name="storyMain"),
]
