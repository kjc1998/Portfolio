from django.shortcuts import redirect

class PathMiddleware:
    """
    Middleware to append '/' to all URLs
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # User Defined Code #

        url = str(request.build_absolute_uri())
        if url[-1] != '/':
            return redirect(url + '/')
        response = self.get_response(request)
        return response