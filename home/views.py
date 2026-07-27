from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'index.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def search(request):
    return render(request, 'search.html')

@login_required
def bookings_page(request):
    return render(request, 'bookings.html')
