import os
import json
import base64
from django.shortcuts import render
from cv.models import CVS


def mainFrame(request, name="kai jie"):
    user = True if name == "kai jie" else False
    cv_file = CVS.objects.get(active=True)
    if cv_file:
        cv_active_b64 = base64.b64encode(cv_file.data).decode("utf-8")
    else:
        cv_active_b64 = None
    return render(request, "mainFrame/mainFrame.html", {
        "name": name.title(),
        "user": user,
        "cv_active_b64": cv_active_b64,
    })
