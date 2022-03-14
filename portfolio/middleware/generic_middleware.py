from django.shortcuts import redirect
from generic_functions import ongoing_project_date_update

class PathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        url = str(request.build_absolute_uri())
        # ALl URLs will now have backslash
        if url[-1] != '/':
            return redirect(url + '/')
        return response

class DateUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        # Update all ongoing project dates
        ongoing_project_date_update()
        return response