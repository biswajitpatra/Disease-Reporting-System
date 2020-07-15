from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from disdata.models import Pincode, Report, Disease
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Count
from datetime import datetime, timedelta


# Create your views here.
def index(request):
    return render(request, 'index.html')


def areaReport(request):
    return render(request, 'areaReport.html')


def hospitalReport(request):
    return render(request, 'hospitalReport.html')


@csrf_exempt
def area_summary_api(req):
    thres_red_reports = 5
    thres_yellow_reports = 2
    thres_time_gap = 30  # Threshold value for reports
    req = json.loads(req.body)
    if ("location" in req):
        tmp = Pincode.objects.annotate(distance=Distance('located_at', p.located_at)).order_by('distance').last()
        req["pincode"] = tmp.pincode
    q = Report.objects.filter(pincode__pincode=req["pincode"]).filter(
        reported_on__gte=datetime.now() - timedelta(days=thres_time_gap))
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
