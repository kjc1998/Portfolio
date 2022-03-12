from datetime import datetime
from django.shortcuts import render
from django.db.models import Q
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError

from generic_functions import error_page, pagination_handling
from project.models import Project, Story, Tags


def projectManagement(request):
    if request.method == "POST":
        if request.user.is_authenticated:
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
                    ongoing = field_entries["projectOngoing_"+project_id]
                    # Default date
                    edit_project.end_date = datetime.now()
                    edit_project.ongoing = True
                except MultiValueDictKeyError:
                    edit_project.end_date = end
                    edit_project.ongoing = False
                edit_project.save()

                # Handling all stories dates after date update
                stories_after = Story.objects.filter(project=project_id, date__gte=edit_project.end_date).all()
                for story_after in stories_after:
                    # set to new end date
                    story_after.date = edit_project.end_date
                    story_after.save()
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
                    return error_page(request, 422, "This file already existed")
        else:
            return error_page(request, 403, "Please login to enter this site")

    # Update Ongoing Project with Time
    ongoing_projects = Project.objects.filter(ongoing=True).all()
    for ongoing_project in ongoing_projects:
        ongoing_project.end_date = datetime.now()
        ongoing_project.save()

    # Pagination
    projects = Project.objects.all().order_by("-start_date")
    projects_page_list, pages = pagination_handling(projects, 5, request)

    # Presentation
    for project in projects_page_list:
        project.start_date = project.start_date.strftime("%Y/%m/%d")
        project.end_date = project.end_date.strftime("%Y/%m/%d")
        project.tag_list = [t.name for t in project.tags.all()]
        if not project.tag_list:
            project.tag_list = ["none"]
    return render(request, "project/projectManagement.html", {
        "projects": projects_page_list,
        "pages": pages,
    })


def projectMain(request, pid):
    try:
        current_project = Project.objects.get(id=pid)
    except Project.DoesNotExist:
        return error_page(request, 500, "No such project exists")

    if request.method == "POST":
        if request.user.is_authenticated:
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

                # Check date (inclusive)
                if not (date.date() >= current_project.start_date and date.date() <= current_project.end_date):
                    return error_page(request, 400, f"Date is out of project range. Project Date: {current_project.start_date} till {current_project.end_date}")

                # Check image
                if image_bytes_data:
                    if "image" not in request.FILES["storyImage_new"].content_type:
                        return error_page(request, 400, "Invalid file type")

                # Add new story
                try:
                    new_story_instance = Story(name=name, date=date, content=content, primary_image=image_bytes_data, project=current_project)
                    new_story_instance.save()
                except IntegrityError:
                    return error_page(request, 422, "This story name has already been taken")

                # Populating tags
                current_story = Story.objects.get(name=name)
                for tag in tags:
                    if tag == "":
                        break
                    try:
                        new_tag_instance = Tags(name=tag)
                        new_tag_instance.save()
                    except IntegrityError:
                        pass
                    
                    # Many-to-Many relationship
                    current_tag = Tags.objects.get(name=tag)
                    current_tag.project.add(current_project)
                    current_tag.story.add(current_story)
        else:
            return error_page(request, 403, "Please login to enter this site")

    # Pagination
    stories = current_project.story.all().order_by("-date")
    story_page_list, pages = pagination_handling(stories, 5, request)

    # Presentation
    for story in story_page_list:
        story.date = story.date.strftime("%Y/%m/%d")
        story.tag_list = [t.name for t in story.tags.all()]
        if not story.tag_list:
            story.tag_list = ['none']

    return render(request, "project/projectMain.html", {
        "project": current_project,
        "stories": story_page_list,
        "pages": pages,
    })

def storyMain(request, pid, sid):
    try:
        current_story = Story.objects.get(id=sid, project=pid)
    except Story.DoesNotExist:
        return error_page(request, 500, "No such Story exists")
    
    return render(request, "mainFrame/mainFrame.html")