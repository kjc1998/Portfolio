import json
import base64
import datetime
from django.shortcuts import render
from django.db.utils import IntegrityError
from django.http import JsonResponse
from .models import CVS


def cvManagement(request):
    if request.user.is_authenticated:
        name = "Kai Jie"
    else:
        name = "Guest"
        return JsonResponse({'error_message': "You need to login first to access into this page"}, status=403)
    if request.method == "POST":
        if "cvUploadName" in request.POST:
            # check pdf type
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
                    return JsonResponse({'error_message': "You have uploaded this version of CV before"}, status=403)
            else:
                return JsonResponse({'error_message': "Only accepts pdf file type"}, status=403)
        else:
            if "activateCV" in request.POST:
                # set active
                cv_id = request.POST["activateCV"]
                try:
                    current_active = CVS.objects.get(active=True)
                    current_active.active = False
                    current_active.save()
                except CVS.DoesNotExist:
                    pass
                new_active_cv = CVS.objects.get(id=int(cv_id))
                new_active_cv.active = True
                new_active_cv.save()
            elif "deleteCV" in request.POST:
                # delete cv
                cv_id = request.POST["deleteCV"]

                delete_cv = CVS.objects.get(id=int(cv_id))
                delete_cv.delete()

                try:
                    current_active = CVS.objects.get(active=True)
                except CVS.DoesNotExist:
                    next_active = CVS.objects.last()
                    if next_active:
                        next_active.active = True
                        next_active.save()
    cv_files = CVS.objects.all()
    dic_of_cvs = {}
    for cv_file in cv_files:
        dic_of_cvs[cv_file.id] = [cv_file.name, cv_file.date.strftime("%m/%d/%Y"), base64.b64encode(
            cv_file.data).decode("utf-8"), cv_file.active]
    return render(request, "cv/cvManagement.html", {
        "name": name.title(),
        "cv_files": json.dumps(dic_of_cvs) if dic_of_cvs else None,
    })
