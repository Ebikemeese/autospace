from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def getBookingTimelines(request):
    return HttpResponse("Hello Booking Timelines")
