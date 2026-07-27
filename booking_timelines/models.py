from django.db import models
from bookings.models import BookingStatus

class BookingTimeline(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='booking_timelines')
    status = models.CharField(max_length=50, choices=BookingStatus.choices)
    manager = models.ForeignKey('managers.Manager', on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_timelines')
    valet = models.ForeignKey('valets.Valet', on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_timelines')

    class Meta:
        indexes = [
            models.Index(fields=['booking']),
        ]

    def __str__(self):
        return f"Timeline {self.id} - Booking {self.booking_id}"
