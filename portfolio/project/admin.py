from django.contrib import admin
from .models import Project, Story, Tags

# Register your models here.
admin.site.register(Project)
admin.site.register(Story)
admin.site.register(Tags)
