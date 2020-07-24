from django.contrib.gis.db import models
from django.contrib.auth.models import User , Group
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import datetime
import requests
import json
import re
import math

'''
s => susceptible (population)
i => infected 
r => recovered
morbidity => morbidity value
incubation => incubation count
t => time passed  in days
'''
def sir_model(s,i,r,morbidity,incubation,t):

    total_population = s

    # his intimacy factor increases in places where trading is more, because trading means more people at work, hence more spread
    intimacy_factor = 4   

    if(t<10):
        beta=0.00005
    else:
        beta=0.00001
    
    # more value means more infectious is the disease
    gamma = 1/incubation
    infection_rate = beta*s*i/total_population
    transmission_index = beta/gamma

    rep_factor = beta*s/gamma

    ret_value = dict()

    if(rep_factor > 1):
        ret_value["spread"]=True
    else:
        ret_value["spread"] = False

    ret_value["infected"] = i+s -((gamma/beta)*(1+math.log(rep_factor)))

    return ret_value

'''
category (borne):
    1:water
    2.vector
    3.viral
rainfall =    //not clear
disease_id = 3 chars 
population = database
age_frq = [<12,12<<25,25<] 
drink = untreated_source drinking
slum  = number of slum
temp: avg temprature of area
area_id :first three digits
'''
def demographic_model(category,rainfall,area_id,disease_id,altitude,population,age_freq,drink,slum,temprature,wind):
    score=0
    if(category==1):
        infant=age_freq[0]
        adult=age_freq[1]
        tw5=age_freq[2]
        if(max(max(infant,adult),tw5)==tw5 or max(max(infant,adult),tw5)==infant):
            score+=1
        
        if(rainfall>=45.0):
            score+=1
            diff=rainfall-45.0
            roll=diff/10
            score= score+(roll*0.42)

        risk = (drink/population)*100
        if(risk>15):
            score+=1

        slum_count =(slum/population)*100
        if(slum_count>8):
            score+=1

    elif(category==2):
        
        if(temprature<=25):
            score+=1
        elif(temprature>30):
            score-=1
        
        if(rainfall>60):
            score-=1
        elif(rainfall>20 and rainfall<60):
            score+=1

    # adjacent cities and compare altitude

    elif(category==3):

        if(temprature>30):
            score-=1
        else:
            trans= 30-temprature
            trans =trans/8
            score+=1
            score = score + trans

        if wind>8.00:
            score+=1
    # print(score)
        
    if(score>=3):
        return 1
    else:
        return 0




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

class District(models.Model):
    name= models.CharField(max_length=30)
    district_official = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    rainfall = models.FloatField()
    altitude= models.IntegerField()
    temprature=models.FloatField()
    population = models.IntegerField()
    water_source = models.IntegerField() # Untreated water source
    humidity = models.FloatField()
    age_frequency_vector = ArrayField(models.IntegerField())
    density = models.IntegerField()
    slums_count = models.IntegerField()
    wind = models.FloatField()
    victim_ids = ArrayField( models.CharField(max_length=2,choices=(('pt',"Poultry"),('gt','Goat'),('pg','Pig'),('bf',"Buffalo"),('sp','Ship'))))
    def __str__(self):
        return self.name

class Pincode(models.Model):
    pincode=models.CharField(max_length=6,validators=[MinLengthValidator(6)],primary_key=True,unique=True)
    area=models.CharField(max_length=40)
    state=models.CharField(max_length=40)
    state_code=models.IntegerField()
    province=models.CharField(max_length=40)
    province2=models.CharField(max_length=40)
    accuracy=models.IntegerField()
    located_at=models.PointField()
    district = models.ForeignKey(District,on_delete=models.CASCADE,null=True)
    is_alerted=models.BooleanField(default=False)
    # adjacent_places=ArrayField(models.ForeignKey('self',on_delete=models.PROTECT),blank=True,default=None)
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
    category= models.CharField(choices = (("1","Water borne"),("Food","Food borne"),("2","Vector borne"),("3","Air borne"),("Animal","Animal transmitted")),max_length=6)
    incubation_period = models.IntegerField()
    mortality = models.FloatField()
    morbidity = models.FloatField()
    threshold_alert = models.IntegerField(default=0)
    vacination_available=models.BooleanField(default=False)
    victim_id=models.CharField(max_length=2,choices=(('pt',"Poultry"),('gt','Goat'),('pg','Pig'),('bf',"Buffalo"),('sp','Sheep')))
    info_spread=models.TextField()
    info_symptoms = models.TextField()
    info_precautions=models.TextField()
    info_diagnostic = models.TextField()
    info_managerial = models.TextField()
    info_url = models.URLField(max_length=200)
    def __str__(self):
        return self.disease_name

def validate_report_category(value):
    if value != None and value != 'human' and value != 'animal':
        raise ValidationError(
            _('%(value)s is not a valid report category, please  use either "human" or "animal"'),
            params={'value': value},
        )

class Report(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True, blank=True)
    reported_on = models.DateTimeField(default=timezone.now)
    # mortality = models.FloatField()
    # morbidity = models.FloatField()
    # infections = models.IntegerField()
    death = models.BooleanField()
    report_info = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True, choices=(("human", "Human"),("animal","Animal")))
    pincode = models.ForeignKey(Pincode,on_delete=models.CASCADE)
    reported_at = models.PointField()
    verified = models.BooleanField(default=True)
    def __str__(self):
        return "{} report from {} reported at {}".format(self.disease, self.source, self.reported_on)
    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)
        if(self.verified==True):
                if(self.category=='human'):
                    district = District.objects.filter(name = self.pincode.province)[0]
                    lst = Outbreak.objects.filter(outbreak_over=False).filter(disease=self.disease)
                    if(lst.count()==0):
                        tmp_new = Outbreak(disease=self.disease,infected=1,death=0,start_report=self,category='human')
                        tmp_new.save()
                        ppls = Person.objects.filter(pincode__pincode__startswith=pincode[:3])
                        for p in ppls:
                            p.notify()
                        new_not = Notice.objects.create(user=district.district_official,attn='warning',msg_notice=True,msg_head='New case detected',msg_body='A new case has been deteced')
                        new_not.save()
                    else:
                        lst=lst[0]
                        if(self.death==True):
                            lst.death+=1
                        else:
                            lst.infected+=1
                        if( lst.infected + lst.death > self.disease.threshold_alert):
                            s = district.population
                            i = lst.infected + lst.death
                            days = datetime.now().date()-timelst.start_report.reported_on
                            res = sir_model(s,i,0,self.disease.morbidity,self.disease.incubation_period,days.days)
                            if res["spread"]==True:
                                if(lst.first_alert==False):    
                                    new_not = Notice.objects.create(user=district.district_official,attn='danger',msg_notice=False,msg_head="Outbreak at your location",msg_body="A outbreak has been detected in your area should we notify?"+res["infected"],action='notify_all_people',action_msg=district.area_id)
                                    new_not.save()
                                    
                                res_pre = demographic_model(int(self.disease.category),district.rainfall,district.area_id,disease.disease_name,district.altitude,district.population,district.age_frequency_vector,district.water_source,district.slums_count,district.temprature,district.wind)                   
                                    # TODO: goverment notice
                                    # TODO: distance based on district 
                                
                            # ppls = Person.objects.filter(pincode__pincode__startswith=self.pincode[:3])
                            # lst.first_alert =True
                            # for people in ppls:
                            #     people.notify()

                            # TODO: notify disease officials
                        lst.save()
                else:
                    lst = Outbreak.objects.filter(outbreak_over=False).filter(disease=self.disease)
                    if(lst.count()==0):
                        tmp_new = Outbreak(disease=self.disease,infected=1,death=0,start_report=self,category='animal')
                        tmp_new.save()
                        ppls = Person.objects.filter(animal_owner=True)
                        for people in ppls:
                            people.notify()
                        district = District.objects.filter(area_id = self.pincode.pincode[:3]).filter(victim_ids__contains=[self.disease.victim_id])[0]
                        new_not = Notice.objects.create(user=district.district_official,attn='warning',msg_notice=True,msg_head='New case detected',msg_body='A new case has been deteced')
                        tmp_new.save()
                        new_not.save()
                    else:
                        lst=lst[0]
                        if(self.death==True):
                            lst.death+=1
                        else:
                            lst.infected+=1
                        if(lst.first_alert==False):    
                            if(lst.infected + lst.death > self.disease.threshold_alert):
                                lst.first_alert =True
                                district = District.objects.filter(area_id = self.pincode.pincode[:3]).filter(victim_ids__contains=[self.disease.victim_id])
                                if(district.count()!=0):
                                    district=district[0]
                                    new_not = Notice.objects.create(user=district.district_official,attn='danger',msg_notice=False,msg_head="Outbreak at your location",msg_body="A outbreak has been detected in your area should we notify?",action='notify_all_people',action_msg=district.area_id)
                                    new_not.save()
                                    # ppls = Person.abjects.filter(pincode__pincode__startswith=district.area_id)
                                    # for p in ppls:
                                    #     p.notify()                                          # notification of  2nd level

                        lst.save()
        # if not self.pk:
        
        # source_user = User.objects.get(id=self.source.pk)
        # risk_population = Person.objects.filter(city=source_user.hospital.city)
        # print("done",risk_population)
        # if self.mortality>10:
        #     for person in risk_population:
        #         person.notify()

class Person(models.Model):
    class Meta:
        verbose_name_plural = "Census"
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
    def notify(self,msg=None):
        #TODO: do it
        pass
        # URL = 'https://www.sms4india.com/api/v1/sendCampaign'
        # response = sendPostRequest(URL, "PT5VPWDIY5UHKR5W9Z7LJA723XAJ4O9L", 'VOT5R4ICAHKB80QP', 'stage', '+919439832766', 'sai.nayak1503@gmail.com', 'Swine flu detected in your vicinity' )
        # print(response.text)

class Outbreak(models.Model):
    disease = models.ForeignKey(Disease,on_delete=models.CASCADE)
    infected = models.IntegerField(default=0)
    death = models.IntegerField(default=0)
    start_report=models.ForeignKey(Report,on_delete=models.CASCADE)
    outbreak_over=models.BooleanField(default=False)
    first_alert=models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=(("human", "Human"),("animal","Animal")))

    def sir_model(self):
        if(self.category=='human'):
            pass
            # District.objectsself.start_report.pincode.pincode[:3]




class Notice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    attn = models.CharField(max_length=7,choices=(('danger','danger'),('warning','warning')))
    msg_notice = models.BooleanField(default=True)
    time = models.DateTimeField(default=timezone.now)
    msg_head = models.CharField(max_length=100)
    msg_body = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    action = models.CharField(max_length=100,blank=True)
    action_msg = models.CharField(max_length=100,blank=True)
    read=models.BooleanField(default=False)

    def notify_all_people(self):
        ppls = Person.objects.filter(pincode__pincode__startswith=self.action_msg)
        for p in ppls:
            p.notify()

    def sample():
        pass





