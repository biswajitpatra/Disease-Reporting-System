from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Disease(models.Model):
    disease_name = models.CharField(max_length=1024)
    mortality = models.FloatField()
    morbidity = models.FloatField()
    info_diagnostic = models.TextField()
    info_managerial = models.TextField()

class Report(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    reported_on = models.DateTimeField()
    mortality = models.FloatField()
    morbidity = models.FloatField()
    infections = models.IntegerField()
