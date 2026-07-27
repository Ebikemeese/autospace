from django.db import models

class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    garage = models.ForeignKey('garages.Garage', on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=0)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Review {self.id} - Rating {self.rating}"
