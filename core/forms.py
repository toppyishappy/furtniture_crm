from pyexpat import model
from django import forms


class PurchaseOrderForm(forms.Form):
    fullname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    tel = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'form-control'}))
    province = forms.CharField(max_length=50)
    district = forms.CharField(max_length=50)
    zone = forms.CharField(max_length=50)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'style': 'width: 471px;'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control', 'type': 'date'}))
    due_date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control', 'type': 'date'}))

    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'style': 'width: 471px;'}), required=False)
 
    # sender = forms.EmailField()
    # cc_myself = forms.BooleanField(required=False)