import json
import base64
import datetime
from django.shortcuts import render
from django.db.utils import IntegrityError
from .models import CVS
from collections import OrderedDict


def cvManagement(request, name="kai jie"):
    user = True if name == "kai jie" else False
    error_message = ""
    if request.method == "POST":
        # two forms that can be submitted in this page
        if "cvUploadName" in request.POST:
            # check count
            count = CVS.objects.all().count()
            if count >= 5:
                error_message = "Cannot upload more than 5 files"
            else:
                # check pdf
                if ".pdf" in str(request.FILES["cvFileUpload"]):
                    try:
                        check_current = CVS.objects.all()
                        if check_current:
                            current_active = CVS.objects.get(active=True)
                            current_active.active = False
                            current_active.save()
                        cv_bytes_data = request.FILES["cvFileUpload"].file
                        new_cv_instance = CVS(name=str(request.FILES["cvFileUpload"]),
                                              date=datetime.datetime.now(), data=cv_bytes_data.read(), active=True)
                        new_cv_instance.save()
                    except IntegrityError:
                        # have existed before
                        error_message = "You have uploaded this version of CV before"
                else:
                    error_message = "Only accepts pdf file type"
        else:
            if "activateCV" in request.POST:
                # set active
                cv_id = request.POST["activateCV"]

                current_active = CVS.objects.get(active=True)
                current_active.active = False
                current_active.save()

                new_active_cv = CVS.objects.get(id=int(cv_id))
                new_active_cv.active = True
                new_active_cv.save()
            elif "deleteCV" in request.POST:
                # delete cv
                cv_id = request.POST["deleteCV"]

                delete_cv = CVS.objects.get(id=int(cv_id))
                delete_cv.delete()
    cv_files = CVS.objects.all()
    dic_of_cvs = {}
    for cv_file in cv_files:
        dic_of_cvs[cv_file.id] = [cv_file.name, cv_file.date.strftime("%m/%d/%Y"), base64.b64encode(
            cv_file.data).decode("utf-8"), cv_file.active]
    return render(request, "cv/cvManagement.html", {
        "name": name.title(),
        "user": user,
        "cv_files": json.dumps(dic_of_cvs),
        "error_message": error_message,
    })
