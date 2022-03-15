import base64
from cv.models import CVS

from generic_functions import database_updates


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

    return {
        "request": request,
        "template": "mainFrame/mainFrame.html",
        "data": {
            "cv_active_b64": cv_active_b64
        }
    }
