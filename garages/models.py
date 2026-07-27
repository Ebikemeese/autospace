from django.db import models

class Garage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='garages')
    description = models.TextField(null=True, blank=True)
    images = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.display_name or f"Garage {self.id}"
