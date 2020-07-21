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

urlpatterns = [
    path('', views.index, name='index'),
    path('hospital/', views.hospitalReport, name='hospitalReport'),
    path('report_delete/',views.delete_report_api, name='delete report'),
    path('report_verify/',views.verify_report_api, name='verify report'),
    re_path(r'^area/(?P<pincode>[0-9]{6})/$', views.areaReport, name='areaReport'),
    path('admin/', admin.site.urls),
    path('user/', views.user, name='user'),
    path('govt/', views.govtReport, name='govtReport'),
    path('login/',LoginView.as_view(template_name='admin/login.html',extra_context={'site_header':'Login form'})),
    path('telephony_bot/',views.telephony_bot,name='Dialogflow bot'),
    path('area_summary_api',views.area_summary_api,name="Area summary API"),
    path('report_api',views.report_api,name="Report API"),
    path('favicon.ico',RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




