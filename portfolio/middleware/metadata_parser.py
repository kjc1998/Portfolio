from typing import Dict, List
from datetime import datetime

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
        and if so, then update self attributes
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
        """
        Parsing data into dictionary for FrontEnd Query
        """
        # Projects handling
        project_list = []
        for project in self._projects:
            project = project.copy()
            del project["ongoing"]
            project["start_date"] = project["start_date"].strftime("%Y-%m-%d")
            project["end_date"] = project["end_date"].strftime("%Y-%m-%d")
            project_list.append(project)

        # Stories handling
        story_list = []
        for story in self._stories:
            story = story.copy()
            del story["primary_image"]
            story["date"] = story["date"].strftime("%Y-%m-%d")
            story_list.append(story)

        # Tags handling
        tag_list = []
        for tag in self._tags:
            tag = tag.copy()
            del tag["id"]
            tag_list.append(tag)

        return {
            "projects": project_list,
            "stories": story_list,
            "tags": tag_list,
        }
