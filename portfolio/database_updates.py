from datetime import datetime
from project.models import Project, Story, Tags

class DatabaseUpdates:
    def __init__(self):
        self._projects, self._stories, self._tags = self._get_database_values()

    def _get_database_values(self):
        """
        Return list objects of projects' data
        """
        projects = list(Project.objects.all().values())
        stories = list(Story.objects.all().values())
        tags = list(Tags.objects.all().values())
        return projects, stories, tags

    def _check_database_updates(self):
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
    
    def _run_database_updates(self):
        def clear_unused_tags():
            """
            Removed unused tags in any story
            """
            tags = Tags.objects.filter(story__isnull=True).all()
            for tag in tags:
                tag.delete()
            return None

        def ongoing_project_date_update():
            """
            Update ongoing project whenever a request
            is sent to server
            """
            ongoing_projects = Project.objects.filter(ongoing=True).all()
            for ongoing_project in ongoing_projects:
                ongoing_project.end_date = datetime.now()
                ongoing_project.save()
            return None

        clear_unused_tags()
        ongoing_project_date_update()
        return None
    
    def _get_metadata(self):
        """
        Return a jsonify object consisting of all relevant informations
        regarding all recorded projects and stories
        """
        updates = self._check_database_updates()
        if updates:
            print("Yes")
        return None