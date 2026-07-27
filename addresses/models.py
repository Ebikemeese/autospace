from django.db import models

class Address(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    garage = models.OneToOneField('garages.Garage', on_delete=models.SET_NULL, null=True, blank=True, related_name='address')
    address = models.CharField(max_length=500)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.address
