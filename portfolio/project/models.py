from django.db import models
from django.db.utils import ProgrammingError

# Create your models here.


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)
    ongoing = models.BooleanField(null=True)


class Story(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(null=False)
    content = models.CharField(max_length=5000)
    primary_image = models.BinaryField(null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="story")


class Tags(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    story = models.ManyToManyField(Story, related_name="tags")
