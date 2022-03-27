import base64

from cv.models import CVS

from generic_functions import database_updates
from project.models import Story


def mainFrame(request):
    """
    URL: /main/

    GET: return main page featuring CV, Projects and Contact details
    """
    try:
        cv_file = CVS.objects.get(active=True)
        cv_active_b64 = base64.b64encode(cv_file.data).decode("utf-8")
    except CVS.DoesNotExist:
        cv_active_b64 = None

    ### GET METHOD ###
    database_updates()

    story_list = Story.objects.all().order_by("-date")[:6]
    for story in story_list:
        if story.primary_image:
            story.image = base64.b64encode(
                story.primary_image).decode("utf-8")
        story.project_name = story.project.name
        story.pid = story.project.id

    return {
        "request": request,
        "template": "mainFrame/mainFrame.html",
        "data": {
            "cv_active_b64": cv_active_b64,
            "story_list": story_list,
        }
    }
