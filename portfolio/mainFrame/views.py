import os
import json
import base64
from django.shortcuts import render


def mainFrame(request, name="kai jie"):
    user = True if name == "kai jie" else False
    cv_file = open(
        "C:/Users/User/Desktop/Coding_Projects/pythonProjects/Portfolio/portfolio/media/cv/CV_KaiJieChow.pdf", "rb").read()
    cv_encode = base64.b64encode(cv_file).decode("utf-8")
    return render(request, "mainFrame/mainFrame.html", {
        "name": name.title(),
        "user": user,
        "cv_encode": cv_encode,
    })
