import os
import json
import base64
from django.shortcuts import render
from cv.models import CVS


def mainFrame(request, name="kai jie"):
    user = True if name == "kai jie" else False
    cv_files = CVS.objects.filter(active=True)
    if cv_files:
        cv_active_b64 = base64.b64encode(cv_files[0].data).decode("utf-8")
    else:
        cv_active_b64 = None
    return render(request, "mainFrame/mainFrame.html", {
        "name": name.title(),
        "user": user,
        "cv_active_b64": cv_active_b64,
    })
