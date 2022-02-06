from random import choices
from django.db import models

# Create your models here.
class ItemModel(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class ItemColor(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class ItemMaterial(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class ItemType(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class ItemImage(models.Model):
    order = models.ForeignKey('core.SaleOrder', related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='items')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Department(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class SaleOrder(models.Model):

    CASH = 0
    CREDIT = 1
    PATMENT_CHOICES = (
        (CASH, 'cash'),
        (CREDIT, 'credit'),
    )

    CASH = 0
    CREDIT = 1
    STATUS_CHOICES = (
        (CASH, 'cash'),
        (CREDIT, 'credit'),
    )

    customer_id = models.IntegerField()
    model_id = models.IntegerField()
    color_id = models.IntegerField()
    material_id = models.IntegerField()
    type_id = models.IntegerField()
    work_location_id = models.IntegerField()
    delivery_date = models.DateField()
    delivery_address = models.TextField()
    payment_method = models.IntegerField(choices=PATMENT_CHOICES)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    deposite_percent = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES)
    comment = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
