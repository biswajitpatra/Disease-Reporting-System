from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator

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

class Pincode(models.Model):
    pincode=models.CharField(max_length=6,validators=[MinLengthValidator(6)],primary_key=True,unique=True)
    area=models.CharField(max_length=40)
    state=models.CharField(max_length=40)
    state_code=models.IntegerField()
    province=models.CharField(max_length=40)
    province2=models.CharField(max_length=40)
    accuracy=models.IntegerField()
    located_at=models.PointField()

    def __str__(self):
        return self.pincode

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    city = models.CharField(max_length=32)
    pincode= models.ForeignKey(Pincode,on_delete=models.CASCADE)
    located_at = models.PointField()
    def __str__(self):
        return self.name

class Disease(models.Model):
    disease_name = models.CharField(max_length=1024)
    zoonotic = models.BooleanField(default=False)
    mortality = models.FloatField()
    morbidity = models.FloatField()
    vacination_available=models.BooleanField(default=False)
    info_spread=models.TextField()
    info_diagnostic = models.TextField()
    info_managerial = models.TextField()
    info_url = models.URLField(max_length=200)
    def __str__(self):
        return self.disease_name

class Report(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    reported_on = models.DateTimeField(default=timezone.now)
    mortality = models.FloatField()
    morbidity = models.FloatField()
    infections = models.IntegerField()
    death = models.BooleanField()
    pincode = models.ForeignKey(Pincode,on_delete=models.CASCADE)
    reported_at = models.PointField()
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
    full_name = models.CharField(max_length=24)
    email = models.EmailField()
    aadhar_number=models.CharField(unique=True,primary_key=True,max_length=12,validators=[MinLengthValidator(12)])
    gender = models.CharField(choices = (("Male","Male"),("Female","Female")),max_length=6)
    phone_number = models.CharField(max_length=10)
    city = models.CharField(max_length=32)
    pincode = models.ForeignKey(Pincode,on_delete=models.CASCADE)
    animal_owner = models.BooleanField()
    located_at = models.PointField()
    def __str__(self):
        return "{} from {}".format(self.full_name, self.city)
    def notify(self):
        URL = 'https://www.sms4india.com/api/v1/sendCampaign'
        response = sendPostRequest(URL, "PT5VPWDIY5UHKR5W9Z7LJA723XAJ4O9L", 'VOT5R4ICAHKB80QP', 'stage', '+919439832766', 'sai.nayak1503@gmail.com', 'Swine flu detected in your vicinity' )
        print(response.text)

