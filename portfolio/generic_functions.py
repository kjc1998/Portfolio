import requests
from datetime import datetime
from typing import List
from django.shortcuts import render
from django.core.paginator import Paginator
from project.models import Story, Project, Tags


def error_page(request: requests.Response, error_status: int, message: str):
    """
    Default error page when a certain exception has been caught
    """
    return render(
        request,
        "defaultError.html", {
            "error_status": error_status,
            "error_message": message
        },
        status=error_status
    )


def pagination_handling(item_files: List, item_per_page: int, request: requests.Response):
    """
    Pagination handling that returns the items in that page
    and the total page number
    """
    paginator = Paginator(item_files, item_per_page)
    pages = range(1, paginator.num_pages+1)
    page_num = request.GET.get("page")
    if page_num:
        # Remove default backslash at the end of URL
        page_num = int(request.GET.get("page").rstrip('/'))
    item_page = paginator.get_page(page_num)
    item_page_list = item_page.object_list
    return item_page_list, pages


def get_stories(current_story: Story):
    """
    Getting the previous and next story 
    given the current story
    """
    pid = current_story.project.id
    stories = Project.objects.get(id=pid).story.all().order_by("date")

    prev_story, next_story = None, None
    for i in range(len(stories)):
        if stories[i].id == current_story.id:
            prev_story = stories[i-1] if i-1 >= 0 else None
            next_story = stories[i+1] if i+1 < len(stories) else None
    return prev_story, next_story


def text_area_line_parser(text_string: str):
    """
    Text area handling for frontend formatting
    """
    text_string = text_string.replace("\n", "<br/>")
    text_string = text_string.replace("\r", "<br/>")
    return text_string


def database_updates():
    def clear_unused_tags():
        """
        Removed unused tags in any story
        """
        tags = Tags.objects.filter(story__isnull=True).all()
        for tag in tags:
            tag.delete()
        return None

    def ongoing_project_date_update():
        """
        Update ongoing project whenever a request
        is sent to server
        """
        ongoing_projects = Project.objects.filter(ongoing=True).all()
        for ongoing_project in ongoing_projects:
            ongoing_project.end_date = datetime.now()
            ongoing_project.save()
        return None

    clear_unused_tags()
    ongoing_project_date_update()
    return None
