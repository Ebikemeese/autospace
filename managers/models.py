from django.db import models

class Manager(models.Model):
    uid = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.OneToOneField('companies.Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='manager')

    def __str__(self):
        return self.display_name or self.uid
