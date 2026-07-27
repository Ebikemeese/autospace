from django.db import models

class Service(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    duration = models.IntegerField()
    garage = models.ForeignKey('garages.Garage', on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    booking = models.ForeignKey('bookings.Booking', on_delete=models.SET_NULL, null=True, blank=True, related_name='services')

    def __str__(self):
        return self.name
