from django.db import models

class ValetAssignment(models.Model):
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, primary_key=True, related_name='valet_assignment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pickup_valet = models.ForeignKey('valets.Valet', on_delete=models.SET_NULL, null=True, blank=True, related_name='pickup_assignments')
    return_valet = models.ForeignKey('valets.Valet', on_delete=models.SET_NULL, null=True, blank=True, related_name='return_assignments')
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    return_lat = models.FloatField(null=True, blank=True)
    return_lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"ValetAssignment for Booking {self.booking_id}"
