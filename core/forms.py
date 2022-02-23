from django import forms
from django.core.validators import RegexValidator

from core.models import ItemColor, ItemMaterial, ItemModel, ItemType

class PurchaseOrderForm(forms.Form):
    fullname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    tel = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}), 
                            validators=[RegexValidator('^0\d{9}$', message='กรุณาตรวจสอบเบอร์โทรศัพ')])
    # province = forms.CharField(max_length=50)
    # district = forms.CharField(max_length=50)
    # zone = forms.CharField(max_length=50)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'style': 'width: 471px;'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control', 'type': 'date'}))
    due_date = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type': 'week'}))

    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'style': 'width: 471px;'}), required=False)
 
    # sender = forms.EmailField()
    # cc_myself = forms.BooleanField(required=False)

class ItemForm(forms.Form):
    pass
    # pass
    # type = forms.ChoiceField(choices=ItemType.get_choices(), widget=forms.Select(attrs={'class':'form-control'}))
    # model = forms.ChoiceField(choices=ItemModel.get_choices(), widget=forms.Select(attrs={'class':'form-control'}))
    # color = forms.ChoiceField(choices=ItemColor.get_choices(), widget=forms.Select(attrs={'class':'form-control'}))
    # material = forms.ChoiceField(choices=ItemMaterial.get_choices(), widget=forms.Select(attrs={'class':'form-control'}))
