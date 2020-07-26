from django import forms
from django.contrib.gis.forms import widgets
from .models import Hospital, Person, Pincode, Report
from django.contrib.gis.geos import Point
from django.contrib.gis.forms import PointField, OSMWidget
from mapwidgets.widgets import GooglePointFieldWidget

class ReportAdminForm(forms.ModelForm):
    reported_at = PointField(required=False, widget=GooglePointFieldWidget, srid=4326)

    class Meta(object):
        model = Report
        exclude = []

class HospitalAdminForm(forms.ModelForm):

    located_at = PointField(required=True, widget=GooglePointFieldWidget, srid=4326)
    class Meta(object):
        model = Hospital
        exclude = []

class PersonAdminForm(forms.ModelForm):

    located_at = PointField(required=True, widget=GooglePointFieldWidget, srid=4326)
    class Meta(object):
        model = Person
        exclude = []

class PincodeAdminForm(forms.ModelForm):

    located_at = PointField(required=True, widget=GooglePointFieldWidget, srid=4326)
    class Meta(object):
        model = Pincode
        exclude = []