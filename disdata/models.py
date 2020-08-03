from django.contrib.gis.db import models
from django.contrib.auth.models import User , Group
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.measure import Distance  

import datetime
import requests
import json
import re
import math
from random import randint

from disdata.projections.SIR import getSIRPlotAsBase64

victim_ids_for_animal={'pt':"Poultry",'gt':'Goat','pg':'Pig','bf':"Buffalo",'sp':'Sheep'}

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
    immune = (total_population*8)/100
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
    print("rep_factor",rep_factor)
    ret_value = dict()

    if(rep_factor > 1):
        ret_value["spread"]=True
    else:
        ret_value["spread"] = False

    ret_value["infected"] = int(i+s -((gamma/beta)*(1+math.log(rep_factor))))-immune

    return ret_value

def sir_model_plot(district_name: str, disease_name: str):

    district_data = District.objects.get(name=district_name)
    total_population = district_data.population

    disease_data = Disease.objects.get(disease_name=disease_name)

    initial_infected_population = Report.objects.filter(disease__disease_name=disease_name, pincode__district__name=district_name, death=False).count()

    initial_susceptible_population = total_population - initial_infected_population

    initial_recovered_population = 0
    
    beta = lambda t: 0.0005

    incubation = disease_data.incubation_period
    
    # more value means more infectious is the disease
    gamma = (1/incubation)

    print(initial_susceptible_population, initial_infected_population, initial_recovered_population, gamma, beta)

    plot = getSIRPlotAsBase64(
        s0=initial_susceptible_population//1000,
        i0=initial_infected_population/1000,
        r0=0,
        gamma=gamma,
        beta=beta
    )

    return plot




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
def demographic_model(category,rainfall,disease_id,altitude,population,age_freq,drink,slum,temprature,wind,density):
    score=0
    category=int(category)
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
        # print(score)
        # if(temprature>30):
        #     score-=1
        # else:
        if(temprature<30):
            trans= 30-temprature
            trans =trans/8
            score+=1
            score = score + trans

        if wind>8.00:
            score+=1

        if density>400:
            score+=(density-400)/200
    print(score)
        
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


def cloneReport(pk, n: int):
    report = Report.objects.get(pk=pk)
    for _ in range(n):
        report.pk = None
        report.save()


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
    category= models.CharField(choices = (("1","Water borne"),("2","Vector borne"),("3","Air borne"),("4","Animal transmitted")),max_length=6)
    incubation_period = models.IntegerField()
    mortality = models.FloatField()
    morbidity = models.FloatField()
    threshold_alert = models.IntegerField(default=0)
    vaccination_available=models.BooleanField(default=False)
    vaccination_regiment = models.CharField(max_length=255,blank=True)
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
                    district = self.pincode.district
                    lst = Outbreak.objects.filter(outbreak_over=False).filter(disease=self.disease)
                    if(lst.count()==0):
                        tmp_new = Outbreak(disease=self.disease,infected=1,death=0,start_report=self,category='human')
                        tmp_new.save()
                        ppls = Person.objects.filter(pincode__district=self.pincode.district)
                        for p in ppls:
                            p.notify(f"{self.disease.disease_name} detected in {self.pincode.area},{self.pincode.province2}. {self.disease.vaccination_regiment} ")
                        new_not = Notice.objects.create(user=district.district_official,attn='warning',msg_notice=True,msg_head=f"{self.disease.disease_name} detected in {self.pincode.area},{self.pincode.province2}",msg_body=f'Expecting a ground reality report at {self.pincode.area},{self.pincode.province2}.')
                        new_not.save()
                    else:
                        lst=lst[0]
                        if(self.death==True):
                            lst.death+=1
                        else:
                            lst.infected+=1
                        if( lst.infected + lst.death > self.disease.threshold_alert):
                            try:
                                s = district.population
                                i = lst.infected + lst.death
                                days=timezone.now()-lst.start_report.reported_on
                                res = sir_model(s,i,0,self.disease.morbidity,self.disease.incubation_period,days.days)
                                print(res)
                                if res["spread"]==True:
                                    if(lst.first_alert==False):
                                        lst.first_alert = True    
                                        res_pre = demographic_model(int(self.disease.category),district.rainfall,self.disease.disease_name,district.altitude,district.population,district.age_frequency_vector,district.water_source,district.slums_count,district.temprature,district.wind,district.density)                   
                                        if res_pre == 1:
                                            uniq_pincodes=Pincode.objects.filter(located_at__distance_lt=(lst.start_report.reported_at,Distance(km=50))).distinct('district')
                                            for p in uniq_pincodes:
                                                new_not = Notice.objects.create(
                                                    user=district.district_official,
                                                    attn='danger',
                                                    msg_notice=False,
                                                    msg_head=f"Outbreak at {self.pincode.area},{self.pincode.province2} detected",
                                                    msg_body=f"{self.disease.disease_name} outbreak has been detected at {self.pincode.area},{self.pincode.province2}. This outbreak can possibly have a maximum infected number of "+ str(int(res["infected"])) + f".\n Verify this message to notify common people.",
                                                    action='notify_all_people',action_msg=f"This outbreak can possibly have a maximum infected number of " + str(int(res["infected"])) + f".{self.disease.info_precautions}.{self.disease.info_symptoms}"
                                                )
                                                new_not.save()
                                            
                                    # TODO: goverment notice 
                                    
                                    
                                # TODO: notify disease officials
                            except:
                                print("Error occured at predictive models")
                        lst.save()
                elif self.category=="animal":
                    lst = Outbreak.objects.filter(outbreak_over=False).filter(disease=self.disease)
                    if(lst.count()==0):
                        tmp_new = Outbreak(disease=self.disease,infected=1,death=0,start_report=self,category='animal')
                        tmp_new.save()
                        ppls = Person.objects.filter(animal_owner=True)
                        for people in ppls:
                            people.notify(f'{self.disease.disease_name} detected in {self.pincode.area},{self.pincode.province2} \n {self.disease.vaccination_regiment} ')
                        # district = District.objects.filter(area_id = self.pincode.pincode[:3]).filter(victim_ids__contains=[self.disease.victim_id])[0]
                        tmp_new.save()
                        if self.disease.victim_id in self.pincode.district.victim_ids:
                            new_not = Notice.objects.create(user=self.pincode.district.district_official,attn='warning',msg_notice=True,msg_head=f'{self.disease.disease_name} detected in {self.pincode.area},{self.pincode.province2}',msg_body=f'Expecting a ground reality report at {self.pincode.area},{self.pincode.province2}.')
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
                                ppls = Person.objects.filter(animal_owner=True)
                                for people in ppls:
                                    people.notify(f'{self.disease.disease_name} outbreak in {self.pincode.area},{self.pincode.province2}.We expect you to stop trading with that area temporarily . We will notify you when conditions will be normal .Things you should know, {self.disease.info_symptoms} ')
                                district= self.pincode.district
                                for dis in District.objects.all():
                                    if self.disease.victim_id in dis.victim_ids:
                                        new_not = Notice.objects.create(user=dis.district_official,attn='danger',msg_notice=False,msg_head=f"Outbreak at {self.pincode.area},{self.pincode.province2} has been reported.",msg_body="Verify this message to notify common people.",action='notify_all_people',action_msg= f"We hope you to maintain a safe proximity from the {victim_ids_for_animal[self.disease.victim_id]}")
                                        new_not.save()
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
        print(self.full_name+" notified "+str(self.phone_number))
        print(msg)
        url = "https://www.fast2sms.com/dev/bulk"
        headers = {
            'cache-control': "no-cache"
        }
        if(msg==None):
            querystring = {"authorization":"RuzSLcCDS9R9fbF0dFiW9MVPUj5Ur4CHu8ATnldUn59qhTfNJW7LHQ3l2fDo","sender_id":"SMSIND","message":"This is test message","language":"english","route":"p","numbers":str(self.phone_number),"language":"unicode"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
        else:
            querystring = {"authorization":"RuzSLcCDS9R9fbF0dFiW9MVPUj5Ur4CHu8ATnldUn59qhTfNJW7LHQ3l2fDo","sender_id":"FSTSMS","message":msg,"language":"english","route":"p","numbers":str(self.phone_number),"language":"unicode"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
        # pass
            # RuzSLcCDS9R9fbF0dFiW9MVPUj5Ur4CHu8ATnldUn59qhTfNJW7LHQ3l2fDo
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
    def __str__(self):
        return f'Outbreak at {self.start_report.pincode.district.name} of {self.disease.disease_name} at {self.start_report.reported_on}'
    def sir_model(self):
        if(self.category=='human'):
            pass
            # District.objectsself.start_report.pincode.pincode[:3]




class Notice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    attn = models.CharField(max_length=7,choices=(('danger','danger'),('warning','warning')))
    msg_notice = models.BooleanField(default=True)
    time = models.DateTimeField(default=timezone.now)
    msg_head = models.CharField(max_length=255)
    msg_body = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    action = models.CharField(max_length=255,blank=True)
    action_msg = models.CharField(max_length=1000,blank=True)
    read=models.BooleanField(default=False)

    def __str__(self):
        return "{} level notice reported at {}".format(self.attn, self.time)
    def notify_all_people(self):
        ppls = Person.objects.filter(pincode__district=District.objects.get(district_official=self.user))
        for p in ppls:
            p.notify(self.action_msg)

    def sample():
        pass





