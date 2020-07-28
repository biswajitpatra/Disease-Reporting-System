"""drd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from disdata import views
# Use static() to add url mapping to serve static files during development (only)
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
# from disdata.views import FoliumView

urlpatterns = [
    path('', views.index, name='index'),
    path('hospital/', views.hospitalReport, name='hospitalReport'),
    path('report_delete/',views.delete_report_api, name='delete report'),
    path('report_verify/',views.verify_report_api, name='verify report'),
    re_path(r'^area/(?P<pincode>[0-9]{6})/$', views.areaReport, name='areaReport'),
    path('admin/', admin.site.urls),
    path('user/', views.user, name='user'),
    path('govt/', views.govtReport, name='govtReport'),
    path('govt/disease_report/<str:diseaseName>',views.mapping),
    path('govt/disease_heatmap/<str:diseaseName>',views.heatMap),
    path('diseases/' , views.diseases),
    # path('govt/hospitalMap', views.hospitalMapping),
    # path('maps/', FoliumView.as_view(), name='choropleth'),
    path('login/',LoginView.as_view(template_name='admin/login.html',extra_context={'site_header':'Login form', 'site_title':'Staff Login Form'})),
    path('telephony_bot/',views.telephony_bot,name='Dialogflow bot'),
    path('area_summary_api',views.area_summary_api,name="Area summary API"),
    path('report_api',views.report_api,name="Report API"),
    path('favicon.ico',RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('user_action',views.usernotice_action,name='Notice action API'),
    path('disease_list',views.disease_list_api,name="List of Diseasea"),
    path('device_report_api',views.device_report_api,name="Report api for devices"),
    path('location_warn_states/<int:pincode>',views.location_warn_state,name='Warn state for location'),
    path('get_notices_api/<int:days>',views.get_notices_api,name='Get notices'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




