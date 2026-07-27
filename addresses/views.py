from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def getAddresses(request):
    return HttpResponse("Hello Addresses")
