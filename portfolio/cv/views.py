import json
import base64
import datetime
from django.shortcuts import render
from django.db.utils import IntegrityError

from generic_functions import error_page, pagination_handling, updates_after
from cv.models import CVS


def cvManagement(request):
    """
    URL: /CV/

    GET: return list of CVs version and currently active CV (viewable by general public)

    POST: Add, Activate and Delete CVs (only accessible when logged in)
    """

    if request.user.is_authenticated:
        pass
    else:
        return error_page(request, 403, "Please login to enter this site")
        
    if request.method == "POST":
        if "cvUploadName" in request.POST:
            # Check pdf type
            if ".pdf" in str(request.FILES["cvFileUpload"]):
                try:
                    check_current = CVS.objects.all()
                    if check_current:
                        current_active = CVS.objects.get(active=True)
                        current_active.active = False
                    cv_bytes_data = request.FILES["cvFileUpload"].file
                    new_cv_instance = CVS(name=str(request.FILES["cvFileUpload"]),
                                          date=datetime.datetime.now(), data=cv_bytes_data.read(), active=True)
                    new_cv_instance.save()
                    current_active.save()
                except IntegrityError:
                    # Undo previous adjustments
                    current_active.active = True
                    current_active.save()
                    return error_page(request, 422, "This file already existed")
            else:
                return error_page(request, 422, "Invalid file type (pdf type only)")
        else:
            if "activateCV" in request.POST:
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
    
    ### GET METHOD ###
    
    # Get latest database updates
    updates_after()

    cv_active = CVS.objects.filter(active=True).first()

    # Pagination
    cv_files = CVS.objects.exclude(active=True).all().order_by("-id")
    cv_page_list, pages = pagination_handling(cv_files, 4, request)

    # Data parsing
    dic_of_cvs = {
        cv_active.id: [cv_active.name,
                       cv_active.date.strftime("%Y-%m-%d"),
                       base64.b64encode(cv_active.data).decode("utf-8"),
                       cv_active.active]
    }
    for cv_file in cv_page_list:
        dic_of_cvs[cv_file.id] = [cv_file.name, cv_file.date.strftime("%Y-%m-%d"), base64.b64encode(
            cv_file.data).decode("utf-8"), cv_file.active]

    return render(request, "cv/cvManagement.html", {
        "pages": pages,
        "cv_files": json.dumps(dic_of_cvs) if dic_of_cvs else None,
    })
