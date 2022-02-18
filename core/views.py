from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from core.forms import PurchaseOrderForm

@method_decorator(login_required, name='dispatch')
class HomePage(View):

    def get(self, request):
        return render(request, 'homepage.html')


@method_decorator(login_required, name='dispatch')
class PurchaseOrder(View):

    def get(self, request):
        form = PurchaseOrderForm()
        return render(request, 'core/purchase-order.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PurchaseOrderDetail(View):

    def get(self, request, id):
        return render(request, 'core/purchase-order-detail.html')


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