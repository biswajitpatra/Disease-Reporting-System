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
    def save(self, *args, **kwargs):
        if not self.pk:
            source_user = User.objects.get(id=self.source.pk)
            risk_population = Person.objects.filter(city=source_user.hospital.city)
            for person in risk_population:
                person.notify()
        super(Report, self).save(*args, **kwargs)

class Person(models.Model):
    full_name = models.CharField(max_length=1024)
    email = models.EmailField()
    gender = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=32)
    def __str__(self):
        return "{} from {}".format(self.full_name, self.city)
    def notify(self):
        # Use this function to notify user
        pass

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=32)