from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect
from disdata.models import Pincode, Report, Disease,Hospital,Notice,District,Outbreak
from django.core import serializers
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Count   
from datetime import datetime, timedelta
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
import requests
import pandas as pd
from django.views.generic import TemplateView
import folium
import folium.plugins as plugins
import os

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
    print("rep_factor",rep_factor)
    ret_value = dict()

    if(rep_factor > 1):
        ret_value["spread"]=True
    else:
        ret_value["spread"] = False

    ret_value["infected"] = int(i+s -((gamma/beta)*(1+math.log(rep_factor))))

    return ret_value




# Create your views here.
def animalOutbreakInfo(request):
    list_of_diseases = list(Disease.objects.filter(category='4'))
    list_of_pincodes = list(Pincode.objects.all())
    return render(request, 'animalReport.html', { "diseases": list_of_diseases, "pincodes":list_of_pincodes })


def diseases(request):
    list_of_diseases = list(Disease.objects.all())
    return render(request, 'diseases.html', { "diseases": list_of_diseases})

def index(request):
    # list_of_news = list(Notice.objects.all().values())
    nt = Notice.objects.all()
    notice_json = serializers.serialize('json',nt)

        # return HttpResponse(ret_json, content_type='application/json')
    list_of_diseases = list(Disease.objects.all())
    list_of_districts = list(District.objects.all())
    list_of_pincodes = list(Pincode.objects.all())
    # print(list_of_pincodes[0].pincode)
    # print(type(notice_json))
    # print(nt.fields.msg_head)
    return render(request, 'index.html', { "diseases": list_of_diseases, "districts": list_of_districts, "pincodes": list_of_pincodes,"notice_json":notice_json, "notices":nt})

def govtReport(request):
    list_of_diseases = list(Disease.objects.all())
    reports = list(Report.objects.filter(verified=True))
    print(list_of_diseases)
    print(reports)

    m = folium.Map(location = [20.9517, 85.0985], zoom_start=5)
    for h in Hospital.objects.all():
        latt = h.located_at.y
        long = h.located_at.x
        folium.Marker([latt, long],popup='<strong class="text-info text-uppercase" > PIC:'+ str(h.user) +'</strong>', tooltip='<strong>'+str(h.name)+', '+ str(h.city)+'</strong>').add_to(m)

    m.save(os.path.join('disdata','static','hospitalMap.html'))

    return render(request, 'govtReport.html', { "diseases": list_of_diseases, "reports": reports}) 

def heatMap(request,diseaseName):
    m = folium.Map(location = [20.9517, 85.0985], tiles='CartoDB Positron', zoom_start=5)
    hospital_data = []
    for h in Hospital.objects.all():
        cnt = Report.objects.filter(verified=True).filter(source=h.user).filter(disease__disease_name=diseaseName).count()
        cnt*10000
        lat =h.located_at.y
        lng =h.located_at.x
        hospital_data.append([lat, lng, cnt]) 
    plugins.HeatMap(hospital_data).add_to(m)
    m.save(os.path.join('disdata','static','heatMap.html'))
    return HttpResponse(status=200)

def mapping(request,diseaseName):
    state = open(os.path.join('data', 'odisha.json')).read()
    # print(os.getcwd())
    
    data_name=[]
    data_number=[]
    state_json = json.loads(state)
    rep =Report.objects.filter(disease__disease_name=diseaseName).filter(verified=True)
    for s in state_json["features"]:
        disi = s["properties"]["district"]
        data_name.append(disi)
        data_number.append(rep.filter(pincode__province__iexact=disi).count())
        s["properties"]["infections"]=data_number[-1]
    
    data=pd.DataFrame({'name':data_name,'number':data_number})
    m = folium.Map(location = [20.9517, 85.0985], zoom_start=7)
    # m.add_to(figure)



    choropleth = folium.Choropleth(
        geo_data = state_json,
        # geojson = 'objects.disctricts',
        name = 'choropleth',
        data = data ,
        columns=['name', 'number'],
        key_on='feature.properties.district',
        fill_color='YlGn',
        fill_opacity=1,
        line_opacity=1,
        legend_name='Infection Rate',
        highlight=True,
    ).add_to(m)

    # folium.GeoJson(
    #     state,
    #     tooltip=folium.features.Tooltip(' Infection ' + )
    # ).add_to(m)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['infections'], labels=False)
    )
    
    # figure.render()
    # return {"map": figure}

    # return render(request, 'govtReport.html', { "diseases": list_of_diseases, "reports": reports,"map":figure}) 
    m.save(os.path.join('disdata','static','choropleth.html'))
    return HttpResponse(status=200)

# def hospitalMapping(request):
#     m = folium.Map(location = [20.9517, 85.0985], zoom_start=7)

#     for h in Hospital.objects.all():
#         latt = h.located_at.y
#         long = h.located_at.x
#         folium.Marker([latt, long],popup='<strong>Location</strong>', tooltip='Click for more information').add_to(m)

#     m.save(os.path.join('disdata','static','hospitalMap.html'))
#     return HttpResponse(status=200)

@login_required(login_url='/login')
def user(requests):
    unread_notices_length = Notice.objects.filter(user=requests.user).filter(read=False).count()
    notices = Notice.objects.filter(user=requests.user).order_by('-time')
    return render(requests,'user-notice.html',{"unread_notices_length":unread_notices_length,"notices":notices})

def usernotice_action(req):
    if(req.user.is_authenticated):
        notice_id = req.POST.get('notice_id')
        res = req.POST.get('response')
        notice= Notice.objects.get(pk=notice_id)
        if(res=="seen" or res=='reject'):
            notice.read=True
            notice.save()
        elif (res=='accept'):
            notice.read= True
            notice.approved =True
            getattr(notice,notice.action)() 
            notice.save()            
        return HttpResponseRedirect("/user")
    else:
        return HttpResponseRedirect("/user?failed")


def check_hospital_staff(user):
    if user.is_authenticated:
        return Hospital.objects.filter(user=user).count()!=0
    else:
        return False

# @login_required
@user_passes_test(check_hospital_staff,login_url='/login')
def hospitalReport(request):
    reports=list(Report.objects.all().filter(source=request.user).filter(verified=False))
    hospitalName = Hospital.objects.get(user=request.user).name
    # print(hospitalName)
    print(reports)
    loca=[]
    for r in reports:
        url=f"https://maps.googleapis.com/maps/api/geocode/json?latlng={r.reported_at.y},{r.reported_at.x}&key=AIzaSyDI0rZJabSHwnaVtPU71KsqokaqowHSQ70"
        res=requests.get(url)
        # print(res.json())
        loca.append(res.json())
        # loca.append([r.reported_at.x,r.reported_at.)
    reports=zip(reports,loca)
    list_of_diseases = list(Disease.objects.all())
    return render(request, 'hospitalReport.html',{'reports':reports, 'hospitalName':hospitalName, 'diseases': list_of_diseases})

def verify_report_api(req):
    if(req.user.is_authenticated):
        rt=Report.objects.get(pk=req.POST.get('report_id'))
        rt.verified=True
        corrected_category = req.POST.get('report_category')
        print('yare yare daze: ', corrected_category)
        if corrected_category is not None:
            rt.category = corrected_category

        corrected_disease = req.POST.get('disease_name')
        if corrected_disease is not None:
            corrected_disease = Disease.objects.get(disease_name=corrected_disease)
            rt.disease = corrected_disease

        rt.save()
        return HttpResponseRedirect('/hospital')
    return HttpResponseRedirect('/hospital?failed')


def delete_report_api(req):
    if(req.user.is_authenticated==False):
        return HttpResponse("Not authorized",status=401)
    else:
        if req.method=='POST':
            Report.objects.get(pk=req.POST.get('report_id')).delete()
    return HttpResponse("done",status=200)

@csrf_exempt
def disease_list_api(req):
    disease_list=list(Disease.objects.all().values_list('disease_name',flat=True))
    return JsonResponse({"disease_list": disease_list})

@csrf_exempt
def device_report_api(req):
    report_pincode = req.POST.get('pincode')
    if report_pincode is not None:
        report_pincode=Pincode.objects.filter(pincode=report_pincode).first()
        report_location = Point(x=report_pincode.located_at.x, y=report_pincode.located_at.y, srid=4326)

        suspected_disease = Disease.objects.get(disease_name=req.POST.get("disease_name"))

        closest_hospital = Hospital.objects.annotate(distance=Distance('located_at', report_location)).order_by('distance').first()
        report_source = closest_hospital.user
        public_report = Report(
            source=report_source,
            disease=suspected_disease,
            death=False,
            pincode=report_pincode,
            report_info=req.POST.get('report_info'),
            reported_at=report_location,
            verified=False
        )
        public_report.save()
        return HttpResponse(status=200)
    return HttpResponse(status=500)

@csrf_exempt
def location_warn_state(req,pincode):
    thres_time_gap= 30       
    district = Pincode.objects.get(pincode=int(pincode)).district
    q = Report.objects.filter(pincode__district=district).filter(reported_on__gte=datetime.now()-timedelta(days=thres_time_gap)).filter(verified=True)
    cnt = q.values('disease__disease_name').annotate(Count('disease')).order_by('-disease__count')
    ret_json=[]
    max_warn=0
    for c in cnt:
        disease = Disease.objects.get(disease_name = c["disease__disease_name"])
        try:
            total_infected_per =(sir_model(district.population,c["disease__count"],0,0,disease.incubation_period,8)/district.population) 
        except:
            total_infected_per = 0 
                
        if(total_infected_per < 0.012):
            ret_part={"warning":"success"} #? Success == green zone
        elif(total_infected_per >= 0.12): 
            ret_part={"warning":"danger"}  #? Danger == red zone
        else:
            ret_part={"warning":"warning"} #? Warning == yellow zone
        
        max_warn=max(total_infected_per,max_warn)

        ret_part["report_count"]=c["disease__count"]
        ret_part["disease"]=Disease.objects.filter(disease_name=c['disease__disease_name']).values()[0]
        ret_part["disease_level"]=disease.morbidity
        ret_json.append(ret_part)
    # print(ret_json)
    # print(ret_json[0]['warning'])
    if(max_warn < 0.012):
        max_warn=0 #? Success == green zone
    elif(max_warn >= 0.12): 
        max_warn=2  #? Danger == red zone
    else:
        max_warn=1
    return JsonResponse({'warn':max_warn})

@csrf_exempt
def get_notices_api(req,days=0):
    if(days==0):
        nt = Notice.objects.all()
        ret_json = serializers.serialize('json',nt)
        return HttpResponse(ret_json, content_type='application/json')
    else:
        nt = Notice.objects.filter(time__gte=datetime.now()-timedelta(days=days))
        ret_json = serializers.serialize('json',nt)
        return HttpResponse(ret_json, content_type='application/json')


@csrf_exempt
def report_api(req):
    if req.method == 'POST':
        # req=json.loads(req.body.decode('utf-8'))
        print('Post body: ', req.POST)
        report_pincode = req.POST.get('pincode')
        if report_pincode is not None:
            report_pincode=Pincode.objects.filter(pincode=report_pincode).first()
            report_location = Point(x=report_pincode.located_at.x, y=report_pincode.located_at.y, srid=4326)

            suspected_disease = Disease.objects.get(disease_name=req.POST.get("disease_name"))

            closest_hospital = Hospital.objects.annotate(distance=Distance('located_at', report_location)).order_by('distance').first()
            report_source = closest_hospital.user
            public_report = Report(
                source=report_source,
                disease=suspected_disease,
                death=False,
                pincode=report_pincode,
                report_info=req.POST.get('report_info'),
                reported_at=report_location,
                verified=False
            )
            public_report.save()
            return HttpResponseRedirect('/?success')
    return HttpResponseRedirect('/?failed')

def areaReport(request,pincode):
    thres_time_gap= 30       # Time gap for reports
    district = Pincode.objects.get(pincode=int(pincode)).district
    q = Report.objects.filter(pincode__district=district).filter(reported_on__gte=datetime.now()-timedelta(days=thres_time_gap)).filter(verified=True)
    cnt = q.values('disease__disease_name').annotate(Count('disease')).order_by('-disease__count')
    ret_json=[]
    max_warn=0
    disease_max_warn = None
    for c in cnt:
        disease = Disease.objects.get(disease_name = c["disease__disease_name"])
        try:
            total_infected_per =(sir_model(district.population,c["disease__count"],0,0,disease.incubation_period,8)/district.population) 
        except:
            total_infected_per = 0 
                
        if(total_infected_per < 0.012):
            ret_part={"warning":"success"} #? Success == green zone
        elif(total_infected_per >= 0.12): 
            ret_part={"warning":"danger"}  #? Danger == red zone
        else:
            ret_part={"warning":"warning"} #? Warning == yellow zone
        print(disease.disease_name,total_infected_per)
        if(total_infected_per>=max_warn):
            disease_max_warn=disease
        max_warn=max(total_infected_per,max_warn)
        
        ret_part["report_count"]=c["disease__count"]
        ret_part["death_count"]=q.filter(disease=disease).filter(death=True).count()
        ret_part["disease"]=Disease.objects.filter(disease_name=c['disease__disease_name']).values()[0]
        ret_part["disease_level"]=disease.morbidity
        ret_json.append(ret_part)
    # print(ret_json)
    # print(ret_json[0]['warning'])
    if(max_warn < 0.012):
        max_warn="success" #? Success == green zone
    elif(max_warn >= 0.12): 
        max_warn="danger"  #? Danger == red zone
    else:
        max_warn="warning"

    pincodes = list(Pincode.objects.all())
    pincode_details = Pincode.objects.get(pincode=pincode)
    outbreaks = Outbreak.objects.filter(start_report__pincode__district=district).filter(start_report__category='human').filter(outbreak_over=True).order_by('-disease__morbidity')
    outbreaks_json = list(outbreaks.values('infected', 'death', 'disease__disease_name','disease__morbidity'))
    print(disease_max_warn)
    return render(request, 'areaReport.html',{"disease_max":disease_max_warn,"pincodes":pincodes,"diseases_json":json.dumps({"disease_list":ret_json,"max_warn":max_warn}),"diseases":ret_json, "pincode_details":pincode_details,"max_warn":max_warn,"outbreaks":outbreaks,"outbreak_json":json.dumps(outbreaks_json)})    


@csrf_exempt
def area_summary_api(req):
    thres_red_reports= 5     # Threshold for red reports
    thres_yellow_reports=2   # THreshold for yellow reports
    thres_time_gap= 30       # Threshold value for reports
    req = json.loads(req.body)
    if("location" in req and "pincode" not in req):
        tmp=Pincode.objects.annotate(distance=Distance('located_at',Point(req["location"]["long"],req["location"]["latt"]))).order_by('distance').last()
        req["pincode"]=tmp.pincode
    q = Report.objects.filter(pincode__pincode=req["pincode"]).filter(reported_on__gte=datetime.now()-timedelta(days=thres_time_gap)).filter(verified=True)
    cnt = q.values('disease__disease_name').annotate(Count('disease'))
    ret_json = dict()
    for c in cnt:
        if (c["disease__count"] < thres_yellow_reports):
            ret_part = {"warning": "green"}
        elif (q.count() >= thres_red_reports):
            ret_part = {"warning": "red"}
        else:
            ret_part = {"warning": "yellow"}

        ret_part["report_count"] = c["disease__count"]
        ret_part["disease"] = Disease.objects.get(disease_name=c['disease__disease_name'])
        ret_json[c['disease__disease_name']] = ret_part

    return JsonResponse(ret_json)


# Function for dialogflow requests
@csrf_exempt
def telephony_bot(req):
    req = json.loads(req.body)
    report_pincode = req.POST.get('pincode')
    if report_pincode is not None:
            report_pincode=Pincode.objects.filter(pincode=report_pincode).first()
            report_location = Point(x=report_pincode.located_at.x, y=report_pincode.located_at.y, srid=4326)

            suspected_disease = Disease.objects.get(disease_name=req.POST.get("disease_name"))

            closest_hospital = Hospital.objects.annotate(distance=Distance('located_at', report_location)).order_by('distance').first()
            report_source = closest_hospital.user
            public_report = Report(
                source=report_source,
                disease=suspected_disease,
                death=False,
                pincode=report_pincode,
                report_info=req.POST.get('report_info'),
                reported_at=report_location,
                verified=False
            )
            public_report.save()
    print(json.dumps(req, indent=4, sort_keys=True))
    ret_json = {}
    if (req["queryResult"]["intent"]["displayName"] == "info_place"):
        ret_text = "testing intent"
    ret_json = {"fulfillmentMessages": [{
        "platform": "TELEPHONY",
        "telephonySynthesizeSpeech": {
            "text": ret_text
        }
    },
        {
            "text": {
                "text": [
                    ret_text
                ]
            }
        }
    ]}
    # fulfillmentText = {'fulfillmentText': 'This is Django test response from webhook.'}
    return JsonResponse(ret_json, safe=False)

    
# class FoliumView(TemplateView):
#     template_name = "maps/choropleth.html"

#     def get_context_data(self, **kwargs):
#         figure = folium.Figure()
#         m = folium.Map(
#             location=[45.372, -121.6972],
#             zoom_start=12,
#             tiles='Stamen Terrain'
#         )
#         m.add_to(figure)

#         folium.Marker(
#             location=[45.3288, -121.6625],
#             popup='Mt. Hood Meadows',
#             icon=folium.Icon(icon='cloud')
#         ).add_to(m)

#         folium.Marker(
#             location=[45.3311, -121.7113],
#             popup='Timberline Lodge',
#             icon=folium.Icon(color='green')
#         ).add_to(m)

#         folium.Marker(
#             location=[45.3300, -121.6823],
#             popup='Some Other Location',
#             icon=folium.Icon(color='red', icon='info-sign')
#         ).add_to(m)
#         figure.render()
#         return {"map": figure}
