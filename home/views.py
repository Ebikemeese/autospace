from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def search(request):
    return render(request, 'search.html')

def bookings_page(request):
    return render(request, 'bookings.html')
