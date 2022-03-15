import base64
from django.shortcuts import render
from cv.models import CVS

from portfolio.instance import database_instance


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

    # Get latest database updates
    database_instance._run_database_updates()
    
    metadata = database_instance._get_metadata()
    return render(request, "mainFrame/mainFrame.html", {
        "cv_active_b64": cv_active_b64,
    })
