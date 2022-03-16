from django.db import models

# Create your models here.
class ItemModel(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_object(id):
        return ItemModel.objects.get(id=id)


class ItemColor(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_object(id):
        return ItemColor.objects.get(id=id)


class ItemMaterial(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_object(id):
        return ItemMaterial.objects.get(id=id)
    

class ItemType(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name
    

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
    NONE = 3
    DEPOSITE_CHOICES = (
        (NONE, 'Please select a choice'),
        (PERCENTAGE, 'percentage'),
        (MONEY, 'money'),
    )
    province = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    amphoe = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    form_date = models.DateField()
    customer_id = models.IntegerField()
    signature_id = models.IntegerField(blank=True, null=True)
    work_location_id = models.IntegerField()
    delivery_start_date = models.DateField()
    delivery_end_date = models.DateField()
    delivery_address = models.TextField()
    payment_method = models.IntegerField(choices=PATMENT_CHOICES, blank=True, null=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    deposite_percent = models.IntegerField(default=0)
    deposite_money = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    deposite_type = models.IntegerField(choices=DEPOSITE_CHOICES, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    comment = models.TextField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

