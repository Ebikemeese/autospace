from django.urls import path
from . import views

app_name = 'managers'

urlpatterns = [
    path("", views.getManagers, name="managers"),
]
