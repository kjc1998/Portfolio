from typing import Dict, List

from project.models import Project, Story, Tags


class MetadataParser:
    def __init__(self):
        self._projects, self._stories, self._tags = self._get_database_values()
        self._metadata = self._get_metadata()

    def _get_database_values(self) -> List:
        """
        Return list objects of projects' data
        """
        projects = list(Project.objects.all().values())
        stories = list(Story.objects.all().values())
        tags = list(Tags.objects.all().values())
        return projects, stories, tags

    def _is_database_modified(self) -> bool:
        """
        Check if database values have any changes
        """
        projects, stories, tags = self._get_database_values()
        if projects == self._projects and stories == self._stories and tags == self._tags:
            return False
        else:
            self._projects = projects
            self._stories = stories
            self._tags = tags
            return True

    def _get_metadata(self) -> Dict:
        return None
