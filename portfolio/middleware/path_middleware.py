from django.shortcuts import redirect

class PathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        url = str(request.build_absolute_uri())
        # handling of backslash in urls
        if url[-1] != '/':
            return redirect(url + '/')
        return response