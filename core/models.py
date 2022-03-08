from django.db import models

# Create your models here.
class ItemModel(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_choices():
        result = [('', 'Please select a choice')]
        objects = ItemModel.objects.values()
        for i in objects:
            result.append((i['id'], i['name']))
        return result

    def get_object(id):
        return ItemModel.objects.get(id=id)


class ItemColor(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_choices():
        result = [('', 'Please select a choice')]
        objects = ItemColor.objects.values()
        for i in objects:
            result.append((i['id'], i['name']))
        return result
    
    def get_object(id):
        return ItemColor.objects.get(id=id)


class ItemMaterial(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_choices():
        result = [('', 'Please select a choice')]
        objects = ItemMaterial.objects.values()
        for i in objects:
            result.append((i['id'], i['name']))
        return result

    def get_object(id):
        return ItemMaterial.objects.get(id=id)
    

class ItemType(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_choices():
        result = [('', 'Please select a choice')]
        objects = ItemType.objects.values()
        for i in objects:
            result.append((i['id'], i['name']))
        return result

    def get_object(id):
        return ItemType.objects.get(id=id)

class ItemImage(models.Model):
    order_detail = models.ForeignKey('core.SaleOrderDetail', related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='items')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_all_images(order_detail):
        return ItemImage.objects.filter(order_detail=order_detail)


class Department(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class WorkLocation(models.Model):
    name = models.CharField(max_length=50)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_choices():
        result = [('', 'Please select a choice')]
        objects = WorkLocation.objects.values()
        for i in objects:
            result.append((i['id'], i['name']))
        return result


class SaleOrderDetail(models.Model):
    sale_order = models.ForeignKey('core.SaleOrder', on_delete=models.CASCADE)
    model_id = models.IntegerField()
    color_id = models.IntegerField()
    material_id = models.IntegerField()
    type_id = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class SaleOrder(models.Model):

    CASH = 0
    CREDIT = 1
    PATMENT_CHOICES = (
        (CASH, 'cash'),
        (CREDIT, 'credit'),
    )

    INITIAL = 0
    WATING_APPROVED = 1
    ON_GOING = 2
    DONE = 3
    FAILED = 4
    STATUS_CHOICES = (
        (INITIAL, 'initial'),
        (WATING_APPROVED, 'wating approved'),
        (ON_GOING, 'on going'),
        (DONE, 'done'),
        (FAILED, 'failed'),
    )
    PERCENTAGE = 0
    MONEY = 1
    DEPOSITE_CHOICES = (
        (PERCENTAGE, 'percentage'),
        (MONEY, 'money'),
    )
    form_date = models.DateField()
    customer_id = models.IntegerField()
    work_location_id = models.IntegerField()
    delivery_start_date = models.DateField()
    delivery_end_date = models.DateField()
    delivery_address = models.TextField()
    payment_method = models.IntegerField(choices=PATMENT_CHOICES, blank=True, null=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    deposite_percent = models.IntegerField(default=0)
    deposite_money = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    deposite_type = models.CharField(default=0, max_length=5)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    comment = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
