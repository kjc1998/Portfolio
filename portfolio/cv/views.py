import os
from django.shortcuts import render


def cvManagement(request, name="kai jie"):
    user = True if name == "kai jie" else False
    return render(request, "cv/cvManagement.html", {
        "name": name.title(),
        "user": user,
    })
