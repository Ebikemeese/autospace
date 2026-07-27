from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def getValetAssignments(request):
    return HttpResponse("Hello Valet Assignments")
