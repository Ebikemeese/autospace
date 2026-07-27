from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def getVerification(request):
    return HttpResponse("Hello Verification")
