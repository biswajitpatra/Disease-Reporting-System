from django import forms
from django.contrib.gis.forms import widgets
from .models import Report
from django.contrib.gis.geos import Point
from django.contrib.gis.forms import PointField, OSMWidget

class ReportAdminForm(forms.ModelForm):

    latitude = forms.FloatField(
        min_value=-90,
        max_value=90,
        required=False
    )
    longitude = forms.FloatField(
        min_value=-180,
        max_value=180,
        required=False
    )

    reported_at = PointField(required=False, widget=OSMWidget, srid=4326)


    class Meta(object):
        model = Report
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coordinates = self.initial.get('reported_at', None)
        if isinstance(coordinates, Point):
            self.initial['longitude'], self.initial['latitude'] = coordinates.tuple

    def clean(self):
        data = super().clean()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        point = data.get('reported_at')
        if latitude and longitude:
            data['reported_at'] = Point(longitude, latitude)
        if not data['reported_at']:
            raise forms.ValidationError(
            'Location is required, Please enter Coordinates or select on Map'
            )
        return data

class PHAdminForm(forms.ModelForm):

    latitude = forms.FloatField(
        min_value=-90,
        max_value=90,
        required=False
    )
    longitude = forms.FloatField(
        min_value=-180,
        max_value=180,
        required=False
    )

    located_at = PointField(required=False, widget=OSMWidget, srid=4326)


    class Meta(object):
        model = Report
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coordinates = self.initial.get('located_at', None)
        if isinstance(coordinates, Point):
            self.initial['longitude'], self.initial['latitude'] = coordinates.tuple

    def clean(self):
        data = super().clean()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        point = data.get('located_at')
        if latitude and longitude:
            data['located_at'] = Point(longitude, latitude)
        if not data['located_at']:
            raise forms.ValidationError(
            'Location is required, Please enter Coordinates or select on Map'
            )
        return data

