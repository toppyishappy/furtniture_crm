from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm

from core.models import ItemColor, ItemMaterial, ItemModel, ItemType, SaleOrder, SaleOrderDetail, WorkLocation
from user.models import Customer, EmployeeSignature


class PurchaseOrderForm(ModelForm):
    fullname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    custom_po = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    tel = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}), 
                            validators=[RegexValidator('^0\d{9}$', message='กรุณาตรวจสอบเบอร์โทรศัพ')])
    # province = forms.CharField(max_length=50)
    # district = forms.CharField(max_length=50)
    # zone = forms.CharField(max_length=50)
    work_location_id = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), queryset=WorkLocation.objects.all(), empty_label="Please select")
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control', 'type': 'date', 'id': 'date'}))
    delivery_date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control week-picker', 'id': 'weeklyDatePicker'}))
    province = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'province'}))
    district = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'district'}))
    amphoe = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'amphoe'}))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'zipcode'}))

    class Meta:
        model = Customer
        fields = '__all__'
    
    def initial_data(customer, sale_order):
        return {'fullname': customer.fullname, 'tel': customer.tel, 'work_location_id': sale_order.work_location_id, 'delivery_address': sale_order.delivery_address, 'date': sale_order.form_date,
                'delivery_date': sale_order.delivery_start_date, 'province': sale_order.province, 'district': sale_order.district, 
                'amphoe': sale_order.amphoe, 'zipcode': sale_order.zipcode}


class ItemForm(forms.Form):
    type_id = forms.ModelChoiceField(queryset=ItemType.objects.all(), widget=forms.Select(attrs={'class':'form-select'}), empty_label="Please select")
    model_id = forms.ModelChoiceField(queryset=ItemModel.objects.all(), widget=forms.Select(attrs={'class':'form-select'}), empty_label="Please select")
    color_id = forms.ModelChoiceField(queryset=ItemColor.objects.all(), widget=forms.Select(attrs={'class':'form-select'}), empty_label="Please select")
    material_id = forms.ModelChoiceField(queryset=ItemMaterial.objects.all(), widget=forms.Select(attrs={'class':'form-select'}), empty_label="Please select")
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}), required=False)
    amount = forms.IntegerField(min_value=1,required=True, initial=1,widget=forms.NumberInput(attrs={'class':'form-control'})) 
    price = forms.DecimalField(min_value=0,required=True, initial=0,decimal_places=2,widget=forms.NumberInput(attrs={'class':'form-control'})) 

class SaleForm(forms.Form):
    deposite_type = forms.ChoiceField(choices=SaleOrder.DEPOSITE_CHOICES, widget=forms.Select(attrs={'class':'form-select', 'onchange':'handleChange(this)'}), required=False) 
    payment_method = forms.ChoiceField(choices=SaleOrder.PATMENT_CHOICES, widget=forms.Select(attrs={'class':'form-select'})) 
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'class':'form-control'}), required=False)
    deposite_percent = forms.IntegerField(required=False, initial=0, min_value=0,max_value=100,widget=forms.NumberInput(attrs={'class':'form-control', 'id': 'deposite-percent'})) 
    deposite_money = forms.DecimalField(required=False, initial=0,min_value=0, widget=forms.NumberInput(attrs={'class':'form-control', 'id': 'deposite-money'})) 
    
    def initial_data(sale_order):
        return {'deposite_percent': sale_order.deposite_percent, 'deposite_type': sale_order.deposite_type, 'payment_method': sale_order.payment_method,
                'deposite_money': sale_order.deposite_money, 'comment': sale_order.comment}
