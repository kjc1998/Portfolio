from django.urls import path
from . import views

app_name = "cv"
urlpatterns = [
    path("", views.cvManagement, name="cvManagement"),
    path("/", views.cvManagement, name="cvManagement")
]
