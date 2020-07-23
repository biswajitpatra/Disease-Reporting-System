from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test,login_required
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect
from disdata.models import Pincode, Report, Disease,Hospital,Notice
# from django.core import serializers
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Count   
from datetime import datetime, timedelta
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
import requests

# Create your views here.
def index(request):
    list_of_diseases = list(Disease.objects.all())
    return render(request, 'index.html', { "diseases": list_of_diseases})

def govtReport(request):
    list_of_diseases = list(Disease.objects.all())
    reports = list(Report.objects.filter(verified=True))
    print(list_of_diseases)
    print(reports)
    return render(request, 'govtReport.html', { "diseases": list_of_diseases, "reports": reports}) 


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

# Done?
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
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/?failed')

def areaReport(request,pincode):
    print(pincode)
    thres_red_reports= 5     # Threshold for red reports
    thres_yellow_reports=2   # THreshold for yellow reports
    thres_time_gap= 30       # Threshold value for reports
    q = Report.objects.filter(pincode__pincode=pincode).filter(reported_on__gte=datetime.now()-timedelta(days=thres_time_gap))
    cnt = q.values('disease__disease_name').annotate(Count('disease')).order_by('-disease__count')
    ret_json=[]
    for c in cnt:
        if(c["disease__count"]<thres_yellow_reports):
            ret_part={"warning":"success"} #? Success == green zone
        elif(c["disease__count"]>=thres_red_reports): 
            ret_part={"warning":"danger"}  #? Danger == red zone
        else:
            ret_part={"warning":"warning"} #? Warning == yellow zone

        ret_part["report_count"]=c["disease__count"]
        ret_part["disease"]=Disease.objects.filter(disease_name=c['disease__disease_name']).values()[0]
        ret_json.append(ret_part)
    # print(ret_json)
    # print(ret_json[0]['warning'])
    return render(request, 'areaReport.html',{'pincode':pincode,"diseases_json":json.dumps({"disease_list":ret_json}),"diseases":ret_json})    


@csrf_exempt
def area_summary_api(req):
    thres_red_reports= 5     # Threshold for red reports
    thres_yellow_reports=2   # THreshold for yellow reports
    thres_time_gap= 30       # Threshold value for reports
    req = json.loads(req.body)
    if("location" in req and "pincode" not in req):
        tmp=Pincode.objects.annotate(distance=Distance('located_at',Point(req["location"]["long"],req["location"]["latt"]))).order_by('distance').last()
        req["pincode"]=tmp.pincode
    q = Report.objects.filter(pincode__pincode=req["pincode"]).filter(reported_on__gte=datetime.now()-timedelta(days=thres_time_gap))
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
def telephony_bot(request):
    req = json.loads(request.body)
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
