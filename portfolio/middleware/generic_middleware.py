from django.shortcuts import redirect

from project.models import Project, Story, Tags

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

class DatabaseUpdateMiddleware:
    """
    Middleware to update database values
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self._projects, self._stories, self._tags = self._get_database_values()
    
    def __call__(self, request):
        ### Request Stage ###

        response = self.get_response(request)

        ### Response Stage ###

        # Check updates
        updates = self._check_database_update()
        response.metadata = "metadata"
        print(response)

        return response
    
    def _get_database_values(self):
        projects = list(Project.objects.all().values())
        stories = list(Story.objects.all().values())
        tags = list(Tags.objects.all().values())
        return projects, stories, tags

    
    def _check_database_update(self):
        projects, stories, tags = self._get_database_values()
        if projects == self._projects and stories == self._stories and tags == self._tags:
            return False
        else:
            self._projects = projects
            self._stories = stories
            self._tags = tags
            return True