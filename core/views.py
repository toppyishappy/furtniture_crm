from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, transaction

from core.forms import PurchaseOrderForm, ItemForm
from core.models import ItemColor, ItemMaterial, ItemModel, ItemType, SaleOrder
from user.models import Customer

@method_decorator(login_required, name='dispatch')
class HomePage(View):

    def get(self, request):
        return render(request, 'homepage.html')


@method_decorator(login_required, name='dispatch')
class PurchaseOrder(View):

    def get(self, request):
        form = PurchaseOrderForm()
        return render(request, 'core/purchase-order.html', {'form': form})
    
    def post(self, request):
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            str_dudate = form.cleaned_data['due_date']
            start_week_date = datetime.strptime(str_dudate + '-1', "%Y-W%W-%w")
            end_week_date = start_week_date + timedelta(days=7)
            try:
                with transaction.atomic():
                    Customer.objects.create()
                    SaleOrder.objects.create()

            except:
                pass
        else:
            print('error')
        return render(request, 'core/purchase-order.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PurchaseOrderDetail(View):

    def get(self, request, id):
        return render(request, 'core/purchase-order-detail.html')


@method_decorator(login_required, name='dispatch')
class PurchaseOrderItem(View):

    def get(self, request, id):
        item_color = ItemColor.objects.all()
        item_type = ItemType.objects.all()
        item_material = ItemMaterial.objects.all()
        item_model = ItemModel.objects.all()
        context = {
            'color': item_color,
            'type': item_type,
            'material': item_material,
            'model': item_model
        }
        return render(request, 'core/purchase-order-item.html', context=context)

    def post(self, request, id):
        form = ItemForm(request.POST)
        # if form.is_valid():
        return render(request, 'core/purchase-order-item.html')


@method_decorator(login_required, name='dispatch')
class PurchaseOrderEdit(View):

    def get(self, request, id):
        return render(request, 'core/purchase-order-edit.html')


@method_decorator(login_required, name='dispatch')
class AdminManagement(View):

    def get(self, request):
        return render(request, 'core/admin-management.html')


@method_decorator(login_required, name='dispatch')
class Management(View):

    def get(self, request):
        return render(request, 'core/management.html')


@method_decorator(login_required, name='dispatch')
class Summary(View):

    def get(self, request):
        return render(request, 'core/summary.html')