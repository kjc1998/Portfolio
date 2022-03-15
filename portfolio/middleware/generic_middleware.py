from django.shortcuts import redirect
from django.shortcuts import render
from typing import Dict

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
        response = self.get_response(request)
        if isinstance(response, Dict):
            req, template, data = response["request"], response["template"], response["data"]

            ### Extra Data to be parsed in to template ###

            # Metadata handling
            if self._metadata_instance._is_database_modified():
                self._metadata_instance._metadata = self._metadata_instance._get_metadata()

            data["metadata"] = self._metadata_instance._metadata
            return render(req, template, data)
        return response
