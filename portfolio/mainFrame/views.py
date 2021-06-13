from django.shortcuts import render


def mainFrame(request, name="kai jie"):
    return render(request, "mainFrame/mainFrame.html", {
        "name": name.title(),
    })
