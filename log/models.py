from django.db import models

# Create your models here.

class AdminLog(models.Model):
    order = models.ForeignKey('core.SaleOrder', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class DepartmentLog(models.Model):
    order = models.ForeignKey('core.SaleOrder', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    department_id = models.IntegerField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)