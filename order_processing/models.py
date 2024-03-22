from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    product = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.product}"