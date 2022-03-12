from dataclasses import field
from email.policy import default
from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm

from core.models import ItemColor, ItemMaterial, ItemModel, ItemType, SaleOrder, WorkLocation
from user.models import EmployeeSignature

class PurchaseOrderForm(forms.Form):
    GEEKS_CHOICES =(
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
    )
    fullname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    tel = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}), 
                            validators=[RegexValidator('^0\d{9}$', message='กรุณาตรวจสอบเบอร์โทรศัพ')])
    # province = forms.CharField(max_length=50)
    # district = forms.CharField(max_length=50)
    # zone = forms.CharField(max_length=50)
    work_place_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), choices=WorkLocation.get_choices())
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'class': 'form-select'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control', 'type': 'date', 'id': 'date'}))
    delivery_date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'weeklyDatePicker'}))
    province = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'province'}))
    district = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'district'}))
    amphoe = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'amphoe'}))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'zipcode'}))

    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'style': 'width: 471px;'}), required=False)
 
    # sender = forms.EmailField()
    # cc_myself = forms.BooleanField(required=False)

class ItemForm(forms.Form):
    type_id = forms.ChoiceField(choices=ItemType.get_choices(), widget=forms.Select(attrs={'class':'form-select'}))
    model_id = forms.ChoiceField(choices=ItemModel.get_choices(), widget=forms.Select(attrs={'class':'form-select'}))
    color_id = forms.ChoiceField(choices=ItemColor.get_choices(), widget=forms.Select(attrs={'class':'form-select'}))
    material_id = forms.ChoiceField(choices=ItemMaterial.get_choices(), widget=forms.Select(attrs={'class':'form-select'}))
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}), required=False)
    amount = forms.IntegerField(min_value=0,required=True, initial=0,widget=forms.NumberInput(attrs={'class':'form-control'})) 
    price = forms.DecimalField(min_value=0,required=True, initial=0,decimal_places=2,widget=forms.NumberInput(attrs={'class':'form-control'})) 

class SaleForm(forms.Form):
    # signature_id = forms.ChoiceField(choices=EmployeeSignature.get_choices(), widget=forms.Select(attrs={'class':'form-select'})) 
    deposite_type = forms.ChoiceField(choices=SaleOrder.DEPOSITE_CHOICES, widget=forms.Select(attrs={'class':'form-select'})) 
    payment_method = forms.ChoiceField(choices=SaleOrder.PATMENT_CHOICES, widget=forms.Select(attrs={'class':'form-select'})) 
    # payment_method = forms.ChoiceField(choices=SaleOrder.PATMENT_CHOICES, widget=forms.Select(attrs={'class':'form-select'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'style': 'width: 471px;'}), required=False)
    deposite_percent = forms.IntegerField(min_value=0,max_value =100,required=True, initial=0,widget=forms.NumberInput(attrs={'class':'form-control'})) 
    deposite_money = forms.DecimalField(min_value=0,required=True, initial=0,decimal_places=2,widget=forms.NumberInput(attrs={'class':'form-control'})) 
