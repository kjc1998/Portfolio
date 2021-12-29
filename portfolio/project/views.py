from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.utils import IntegrityError


def projectManagement(request):
    # test render
    return render(request, "mainFrame/mainFrame.html", {
        "cv_active_b64": None,
    })
