import os
import json
import base64
from django.shortcuts import render
from cv.models import CVS


def mainFrame(request, name="kai jie"):
    try:
        cv_file = CVS.objects.get(active=True)
        cv_active_b64 = base64.b64encode(cv_file.data).decode("utf-8")
    except CVS.DoesNotExist:
        cv_active_b64 = None
    return render(request, "mainFrame/mainFrame.html", {
        "cv_active_b64": cv_active_b64,
    })
