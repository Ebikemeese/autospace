from django.db import models

class Valet(models.Model):
    uid = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255)
    company = models.ForeignKey('companies.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='valets')
    image = models.URLField(max_length=500, null=True, blank=True)
    licence_id = models.CharField(max_length=255, default="")

    class Meta:
        unique_together = ('company', 'uid')

    def __str__(self):
        return self.display_name or self.uid
