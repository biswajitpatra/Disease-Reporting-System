from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Disease(models.Model):
    disease_name = models.CharField(max_length=1024)
    mortality = models.FloatField()
    morbidity = models.FloatField()
    info_diagnostic = models.TextField()
    info_managerial = models.TextField()
    def __str__(self):
        return self.disease_name

class Report(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    reported_on = models.DateTimeField(default=timezone.now)
    mortality = models.FloatField()
    morbidity = models.FloatField()
    infections = models.IntegerField()
    def __str__(self):
        return "{} report from {} reported at {}".format(self.disease, self.source, self.reported_on)
