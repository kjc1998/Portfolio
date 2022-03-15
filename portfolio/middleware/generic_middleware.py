from django.shortcuts import redirect
from generic_functions import ongoing_project_date_update, clear_unused_tags

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

class DatabaseUpdateMiddleware:
    """
    Middleware to update database values
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        # Making sure all project are up to dates
        ongoing_project_date_update()
        # Removing unused tags
        clear_unused_tags()
        return response