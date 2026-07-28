from django.urls import path
from . import views

app_name = 'garages'

urlpatterns = [
    path('garages/create/', views.create_garage, name='create_garage'),
    path('garages/<int:garage_id>/', views.garage_detail, name='garage_detail'),
]
