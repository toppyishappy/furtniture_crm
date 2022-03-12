from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    fullname = models.CharField(max_length=50)
    tel = models.CharField(max_length=10)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_object(id):
        return Customer.objects.get(id)


class EmployeeSignature(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='signatures')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_choices():
        result = [('', 'Please select a choice')]
        objects = EmployeeSignature.objects.values()
        for i in objects:
            result.append((i['id'], i['name']))
        return result
