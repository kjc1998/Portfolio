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
            start = datetime.strptime(
                field_entries["projectStart_"+project_id], "%Y-%m-%d")
            end = datetime.strptime(
                field_entries["projectEnd_"+project_id], "%Y-%m-%d") if field_entries["projectEnd_"+project_id] else None

            edit_project = Project.objects.filter(id=int(project_id)).first()
            edit_project.name = name
            edit_project.start_date = start
            try:
                ongoing = field_entries["projectOngoing_"+project_id]

                edit_project.end_date = None
                edit_project.ongoing = True
            except MultiValueDictKeyError:

                edit_project.end_date = end
                edit_project.ongoing = False

            edit_project.save()
        elif "deleteProject" in request.POST:
            delete_project = Project.objects.filter(
                id=int(request.POST["deleteProject"])).first()
            delete_project.delete()
        elif "addProject" in request.POST:
            try:
                field_entries = request.POST
                name = field_entries["projectName_new"]
                start = datetime.strptime(
                    field_entries["projectStart_new"], "%Y-%m-%d")
                end = datetime.strptime(
                    field_entries["projectEnd_new"], "%Y-%m-%d") if field_entries["projectEnd_new"] else None
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
        project.start_date = project.start_date.strftime("%Y-%m-%d")
        project.end_date = project.end_date.strftime(
            "%Y-%m-%d") if project.end_date != None else None
    return render(request, "project/projectManagement.html", {
        "project_list": projects_page_list,
        "pages": pages,
    })


def projectMain(request, pid):
    try:
        current_project = Project.objects.get(id=pid)
    except Project.DoesNotExist:
        return render(request, "defaultError.html", {
            "error_status": 500,
            "error_message": "No such project exists",
        }, status=500)
    stories = current_project.story.all()
    return render(request, "project/projectMain.html", {
    })
