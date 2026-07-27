from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def getGarages(request):
    return HttpResponse("Hello Garages")
