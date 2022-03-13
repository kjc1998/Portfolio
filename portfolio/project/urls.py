from django.urls import path
from . import views

app_name = "project"

urlpatterns = [
    path("", views.projectList, name="projectList"),
    path("<int:pid>/", views.storyList, name="storyList"),
    path("<int:pid>/<int:sid>/", views.storyMain, name="storyMain"),
]
