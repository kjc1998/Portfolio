from django.db import models
from django.db.utils import ProgrammingError

# Create your models here.


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField()
    ongoing = models.BooleanField()


class Story(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField(null=False)
    content = models.CharField(max_length=5000)
    primary_image = models.BinaryField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="story")
