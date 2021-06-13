from django.shortcuts import render
from django.http import HttpResponse


def mainFrame(request):
    return HttpResponse("Hello World!")
