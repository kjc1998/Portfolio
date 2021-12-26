import json
import base64
import datetime
from django.shortcuts import render
from .models import CV_VERSION


def cvManagement(request, name="kai jie"):
    user = True if name == "kai jie" else False
    if request.method == "POST":
        # new pdf instance
        cv_bytes_data = request.FILES["cvFileUpload"].file
        new_cv_instance = CV_VERSION(
            date=datetime.datetime.now(), data=cv_bytes_data.read(), active=True)
        new_cv_instance.save()
    cv_files = CV_VERSION.objects.all()
    dic_of_cvs = {}
    for cv_file in cv_files:
        dic_of_cvs[cv_file.id] = [cv_file.date.strftime("%m/%d/%Y"), base64.b64encode(
            cv_file.data).decode("utf-8"), cv_file.active]
    return render(request, "cv/cvManagement.html", {
        "name": name.title(),
        "user": user,
        "cv_files": json.dumps(dic_of_cvs)
    })
