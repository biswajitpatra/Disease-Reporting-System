from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from disdata.models import Pincode, Report, Disease
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Count   
from datetime import datetime, timedelta
from django.contrib.gis.geos import Point


# Create your views here.
def index(request):
    return render(request, 'index.html')

def hospitalReport(request):
    return render(request, 'hospitalReport.html')


def areaReport(request,pincode):
    print(pincode)
    thres_red_reports= 5     # Threshold for red reports
    thres_yellow_reports=2   # THreshold for yellow reports
    thres_time_gap= 30       # Threshold value for reports
    q = Report.objects.filter(pincode__pincode=pincode).filter(reported_on__gte=datetime.now()-timedelta(days=thres_time_gap))
    cnt = q.values('disease__disease_name').annotate(Count('disease'))
    ret_json=[]
    for c in cnt:
        if(c["disease__count"]<thres_yellow_reports):
            ret_part={"warning":"success"} #? Success == green zone
        elif(q.count()>=thres_red_reports): 
            ret_part={"warning":"danger"}  #? Danger == red zone
        else:
            ret_part={"warning":"warning"} #? Warning == yellow zone

        ret_part["report_count"]=c["disease__count"]
        ret_part["disease"]=Disease.objects.filter(disease_name=c['disease__disease_name']).values()[0]
        ret_json.append(ret_part)
    print(ret_json)
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
