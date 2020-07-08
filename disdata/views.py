from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def areaReport(request):
    return render(request, 'areaReport.html')    
    
@csrf_exempt
def telephony_bot(request):
    req =json.loads(request.body)
    print(json.dumps(req, indent=4, sort_keys=True))
    ret_json={}
    if(req["queryResult"]["intent"]["displayName"]=="info_place"):
        ret_text="testing intent"
    ret_json={"fulfillmentMessages": [{
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
