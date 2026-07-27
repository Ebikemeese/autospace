from django.db import models

class Verification(models.Model):
    garage = models.OneToOneField('garages.Garage', on_delete=models.CASCADE, primary_key=True, related_name='verification')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    admin = models.ForeignKey('authentication.Admin', on_delete=models.CASCADE, related_name='verifications')

    def __str__(self):
        return f"Verification for Garage {self.garage_id} ({self.verified})"
