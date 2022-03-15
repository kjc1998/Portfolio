import copy
from typing import Dict
from urllib.parse import urlparse

from django.shortcuts import redirect
from django.shortcuts import render

from middleware.metadata_parser import MetadataParser


class PathMiddleware:
    """
    Middleware to append '/' to all URLs
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = str(request.build_absolute_uri())
        if url[-1] != '/':
            return redirect(url + '/')
        response = self.get_response(request)
        return response


class HttpResponseMiddleware:
    """
    Middleware for handling dictionary
    and returning as HttpResponse
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Metadata instance
        self._metadata_instance = MetadataParser()

    def __call__(self, request):
        base_url = f"http://{urlparse(request.build_absolute_uri()).netloc}"
        response = self.get_response(request)
        if isinstance(response, Dict):
            req, template, data = response["request"], response["template"], response["data"]

            ### Extra Data to be parsed in to template ###

            # Metadata handling
            if self._metadata_instance._is_database_modified():
                self._metadata_instance._metadata = self._metadata_instance._get_metadata()
            metadata = copy.deepcopy(self._metadata_instance._metadata)

            for project in metadata["projects"]:
                project["url"] = base_url + f"/project/{str(project['id'])}/"
                del project["id"]
            for story in metadata["stories"]:
                story["url"] = base_url + \
                    f"/project/{str(story['project'])}/{str(story['id'])}/"
                del story["project"]
                del story["id"]

            data["metadata"] = metadata
            return render(req, template, data)
        return response
