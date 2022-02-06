from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    fullname = models.CharField(max_length=50)
    tel = models.CharField(max_length=10)
    address = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class EmployeeSignature(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='signatures')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
