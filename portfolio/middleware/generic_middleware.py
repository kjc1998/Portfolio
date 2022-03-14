from django.shortcuts import redirect
from generic_functions import ongoing_project_date_update

class PathMiddleware:
    """
    Middleware to append '/' to all URLs
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        url = str(request.build_absolute_uri())
        if url[-1] != '/':
            return redirect(url + '/')
        return response

class DateUpdateMiddleware:
    """
    Middleware to update project dates
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        ongoing_project_date_update()
        return response