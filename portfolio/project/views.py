from datetime import datetime
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from .models import Project


def projectManagement(request):
    if request.method == "POST":
        if "editProject" in request.POST:
            field_entries = request.POST
            project_id = field_entries["projectID"]
            name = field_entries["projectName_"+project_id]
            start = field_entries["projectStart_"+project_id]
            end = field_entries["projectEnd_"+project_id]
            try:
                ongoing = field_entries["projectOngoing_"+project_id]
            except MultiValueDictKeyError:
                ongoing = False

            edit_project = Project.objects.filter(id=int(project_id)).first()
            edit_project.name = name
            edit_project.start_date = start
            edit_project.end_date = end
            edit_project.ongoing = True if ongoing else False
            edit_project.save()
        elif "deleteProject" in request.POST:
            delete_project = Project.objects.filter(
                id=int(request.POST["deleteProject"])).first()
            delete_project.delete()
        elif "addProject" in request.POST:
            try:
                field_entries = request.POST
                name = field_entries["projectName_new"]
                start = field_entries["projectStart_new"]
                end = field_entries["projectEnd_new"]
                try:
                    ongoing = field_entries["projectOngoing_new"]
                except MultiValueDictKeyError:
                    ongoing = False

                if ongoing:
                    new_project = Project(
                        name=name, start_date=start, ongoing=True)
                else:
                    new_project = Project(
                        name=name, start_date=start, end_date=end, ongoing=False)
                new_project.save()
            except IntegrityError:
                return render(request, "defaultError.html", {
                    "error_status": 422,
                    "error_message": "This file already existed",
                }, status=422)
    projects = Project.objects.all().order_by("-start_date")
    projects_paginator = Paginator(projects, 5)
    pages = range(1, projects_paginator.num_pages + 1)

    # Pagination
    page_num = request.GET.get("page")
    project_page = projects_paginator.get_page(page_num)
    projects_page_list = project_page.object_list
    for project in projects_page_list:
        project.start_date = str(project.start_date)
        project.end_date = str(
            project.end_date) if project.end_date != None else None
    return render(request, "project/projectManagement.html", {
        "project_list": projects_page_list,
        "pages": pages,
    })
