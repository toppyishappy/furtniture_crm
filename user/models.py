from django.db import models

# Create your models here.
class Customer(models.Model):
    fullname = models.CharField(max_length=50)
    tel = models.CharField(max_length=10)
    address = models.TextField()
    delivery_date = models.DateField()

    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)