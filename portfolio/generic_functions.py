import requests
from typing import List
from django.shortcuts import render
from django.core.paginator import Paginator
from project.models import Story, Project

def error_page(request: requests.Response, error_status: int, message: str):
    return render(
        request,
        "defaultError.html",{
            "error_status": error_status,
            "error_message": message
        }, 
        status=error_status
    )

def pagination_handling(item_files: List, item_per_page: int, request: requests.Response):
    paginator = Paginator(item_files, item_per_page)
    pages = range(1, paginator.num_pages+1)

    page_num = request.GET.get("page")
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
            prev_story = stories[i-1] if i-1>=0 else None
            next_story = stories[i+1] if i+1<len(stories) else None
    return prev_story, next_story

def text_area_line_parser(text_string: str):
    text_string = text_string.replace("\n", "<br/>")
    text_string = text_string.replace("\r", "<br/>")
    return text_string