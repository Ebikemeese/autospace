from django.db import models

class SlotType(models.TextChoices):
    CAR = 'CAR', 'Car'
    HEAVY = 'HEAVY', 'Heavy'
    BIKE = 'BIKE', 'Bike'
    BICYCLE = 'BICYCLE', 'Bicycle'

class Slot(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    price_per_hour = models.FloatField()
    type = models.CharField(max_length=20, choices=SlotType.choices, default=SlotType.CAR)
    length = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    garage = models.ForeignKey('garages.Garage', on_delete=models.CASCADE, related_name='slots')

    def __str__(self):
        return self.display_name or f"Slot {self.id}"
