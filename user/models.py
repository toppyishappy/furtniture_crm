from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings

class User(AbstractUser):
      SALE = 1
      ADMIN = 2
      
      ROLE_CHOICES = (
          (SALE, 'Sale'),
          (ADMIN, 'Admin'),
      )
      role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


class Customer(models.Model):
    fullname = models.CharField(max_length=50)
    tel = models.CharField(max_length=10)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_object(id):
        return Customer.objects.get(id)


class EmployeeSignature(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='signatures')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_choices():
        result = [('', 'Please select a choice')]
        objects = EmployeeSignature.objects.values()
        for i in objects:
            user = User.objects.get(id=i['user_id'])
            result.append((i['id'], user.first_name))
        return result
