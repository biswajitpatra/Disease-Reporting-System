from django.contrib.gis.admin import OSMGeoAdmin, StackedInline
from django.contrib.gis.forms.widgets import OSMWidget 
from django.contrib.gis.db.models import PointField
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

from .models import Disease, Report, Person, Hospital,Pincode
from .forms import ReportAdminForm, PHAdminForm

admin.site.register(Disease)

class PincodeAdmin(OSMGeoAdmin):
    model=Pincode

admin.site.register(Pincode,PincodeAdmin)

class ReportAdmin(OSMGeoAdmin):
    form = ReportAdminForm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "source" and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Report, ReportAdmin)

class HospitalInline(StackedInline):
    model = Hospital
    can_delete = False
    verbose_name_plural = 'hospital'
    form = PHAdminForm
    formfield_overrides = {
        PointField: {"widget": OSMWidget},
    }

class UserAdmin(BaseUserAdmin):
    inlines = (HospitalInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class PersonAdmin(OSMGeoAdmin):
    form = PHAdminForm
admin.site.register(Person, PersonAdmin)

admin.site.site_header = "Outbreak Report Interface"
admin.site.site_title = "Outbreak Reporting Web Interface"
admin.site.index_title = "Welcome to Outbreak Reporting Web Interface"