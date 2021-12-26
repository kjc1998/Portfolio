from django.db import models

# Create your models here.


class CV_VERSION(models.Model):
    date = models.DateField(null=False)
    data = models.FileField()
    active = models.BooleanField()
