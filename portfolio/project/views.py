from datetime import datetime
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError

from .models import Project, Story, Tags


def projectManagement(request):
    if request.method == "POST":
        if "editProject" in request.POST:
            field_entries = request.POST
            project_id = field_entries["projectID"]
            name = field_entries["projectName_"+project_id]
            start = datetime.strptime(
                field_entries["projectStart_"+project_id], "%Y-%m-%d")
            end = datetime.strptime(
                field_entries["projectEnd_"+project_id], "%Y-%m-%d")

            edit_project = Project.objects.filter(id=int(project_id)).first()
            edit_project.name = name
            edit_project.start_date = start
            try:
                # Check Input
                ongoing = field_entries["projectOngoing_"+project_id]
                edit_project.end_date = datetime.now()  # Default to Current Date
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
                    field_entries["projectEnd_new"], "%Y-%m-%d")
                try:
                    ongoing = field_entries["projectOngoing_new"]
                    ongoing = True
                except MultiValueDictKeyError:
                    ongoing = False
                new_project = Project(
                    name=name, start_date=start, end_date=end, ongoing=ongoing)
                new_project.save()
            except IntegrityError:
                return render(request, "defaultError.html", {
                    "error_status": 422,
                    "error_message": "This file already existed",
                }, status=422)

    # Update Ongoing Project with Time
    ongoing_projects = Project.objects.filter(ongoing=True).all()
    for ongoing_project in ongoing_projects:
        ongoing_project.end_date = datetime.now()
        ongoing_project.save()

    projects = Project.objects.all().order_by("-start_date")
    projects_paginator = Paginator(projects, 5)
    pages = range(1, projects_paginator.num_pages + 1)

    # Pagination
    page_num = request.GET.get("page")
    project_page = projects_paginator.get_page(page_num)
    projects_page_list = project_page.object_list
    for project in projects_page_list:
        project.start_date = project.start_date.strftime("%Y-%m-%d")
        project.end_date = project.end_date.strftime("%Y-%m-%d")
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
    if request.method == "POST":
        if "storyNew_add" in request.POST:
            field_entries = request.POST
            name = str(field_entries["storyName_new"])
            date = datetime.strptime(field_entries["storyDate_new"], "%Y-%m-%d")
            tags = [tag.strip() for tag in field_entries["storyTags_final"].split(",")]
            content = str(field_entries["storyContent_new"])
            try:
                image_bytes_data = request.FILES["storyImage_new"].file.read()
            except KeyError:
                image_bytes_data = None

            # check date
            if not (date.date() > current_project.start_date and date.date() < current_project.end_date):
                return render(request, "defaultError.html", {
                    "error_status": 400,
                    "error_message": f"Date is out of project range. Project Date: {current_project.start_date} till {current_project.end_date}",
                }, status=400)

            # check image
            if image_bytes_data:
                if "image" not in request.FILES["storyImage_new"].content_type:
                    return render(request, "defaultError.html", {
                        "error_status": 400,
                        "error_message": f"Invalid file type",
                    }, status=400)

            # add new story
            try:
                new_story_instance = Story(name=name, date=date, content=content, primary_image=image_bytes_data, project=current_project)
                new_story_instance.save()
            except IntegrityError:
                return render(request, "defaultError.html", {
                    "error_status": 422,
                    "error_message": "This story name already existed",
                }, status=422)

            # populating tags
            current_story = Story.objects.get(name=name)
            for tag in tags:
                if tag == "":
                    break

                try:
                    new_tag_instance = Tags(name=tag)
                    new_tag_instance.save()
                except IntegrityError:
                    pass
                
                # tying tags to projects and stories
                current_tag = Tags.objects.get(name=tag)
                current_tag.project.add(current_project)
                current_tag.story.add(current_story)
                
    stories = current_project.story.all()
    project_tags = current_project.tags.all()
    return render(request, "project/projectMain.html", {
        "project": current_project,
        "stories": stories,
        "tags": project_tags,
    })
