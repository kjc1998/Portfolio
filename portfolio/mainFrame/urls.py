from django.urls import path
from . import views

urlpatterns = [
    path("", views.mainFrame, name="mainFrame")
]
