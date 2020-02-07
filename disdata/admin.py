from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from .models import Disease, Report

admin.site.register(Disease)

class ReportAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "source" and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Report, ReportAdmin)