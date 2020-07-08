from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def areaReport(request):
    return render(request, 'areaReport.html')    