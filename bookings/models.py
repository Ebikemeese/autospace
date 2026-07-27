from django.db import models

class BookingStatus(models.TextChoices):
    BOOKED = 'BOOKED', 'Booked'
    VALET_ASSIGNED_FOR_CHECK_IN = 'VALET_ASSIGNED_FOR_CHECK_IN', 'Valet Assigned For Check In'
    VALET_PICKED_UP = 'VALET_PICKED_UP', 'Valet Picked Up'
    CHECKED_IN = 'CHECKED_IN', 'Checked In'
    VALET_ASSIGNED_FOR_CHECK_OUT = 'VALET_ASSIGNED_FOR_CHECK_OUT', 'Valet Assigned For Check Out'
    CHECKED_OUT = 'CHECKED_OUT', 'Checked Out'
    VALET_RETURNED = 'VALET_RETURNED', 'Valet Returned'

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price_per_hour = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    slot = models.ForeignKey('slots.Slot', on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='bookings')
    vehicle_number = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    passcode = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=BookingStatus.choices, default=BookingStatus.BOOKED)

    class Meta:
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
        ]

    def __str__(self):
        return f"Booking {self.id} - {self.vehicle_number}"
