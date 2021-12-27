from django.db import models

# Create your models here.


class CVS(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField(null=False)
    data = models.BinaryField(null=False, unique=True)
    active = models.BooleanField()
