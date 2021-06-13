from django.shortcuts import render


def mainFrame(request, name="kai jie"):
    user = True if name == "kai jie" else False
    return render(request, "mainFrame/mainFrame.html", {
        "name": name.title(),
        "user": user,
    })
