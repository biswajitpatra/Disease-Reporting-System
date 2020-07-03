from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import requests
import json
# Create your models here.
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)
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
    reported_at = models.PointField()
    mortality = models.FloatField()
    morbidity = models.FloatField()
    infections = models.IntegerField()
    def __str__(self):
        return "{} report from {} reported at {}".format(self.disease, self.source, self.reported_on)
    def save(self, *args, **kwargs):
        # if not self.pk:
        source_user = User.objects.get(id=self.source.pk)
        risk_population = Person.objects.filter(city=source_user.hospital.city)
        print("done",risk_population)
        if self.mortality>10:
            for person in risk_population:
                person.notify()
        super(Report, self).save(*args, **kwargs)

class Person(models.Model):
    full_name = models.CharField(max_length=1024)
    email = models.EmailField()
    gender = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=32)
    located_at = models.PointField()
    def __str__(self):
        return "{} from {}".format(self.full_name, self.city)
    def notify(self):
        URL = 'https://www.sms4india.com/api/v1/sendCampaign'
        response = sendPostRequest(URL, "PT5VPWDIY5UHKR5W9Z7LJA723XAJ4O9L", 'VOT5R4ICAHKB80QP', 'stage', '+919439832766', 'sai.nayak1503@gmail.com', 'Swine flu detected in your vicinity' )
        print(response.text)


class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=32)
    located_at = models.PointField()