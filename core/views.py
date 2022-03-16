from datetime import datetime, timedelta
from decimal import Decimal
from dateutil import relativedelta

from django.shortcuts import redirect, render
from django.views.generic import View, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, transaction
from django.utils import timezone

from core.forms import PurchaseOrderForm, ItemForm, SaleForm
from core.models import Department, ItemColor, ItemImage, ItemMaterial, ItemModel, ItemType, SaleOrder, SaleOrderDetail, WorkLocation
from user.models import Customer, EmployeeSignature, User

@method_decorator(login_required, name='dispatch')
class HomePage(View):

    def get(self, request):
        role = request.user.role
        context = {
            'role': role
        }
        return render(request, 'homepage.html', context=context)


@method_decorator(login_required, name='dispatch')
class PurchaseOrder(View):

    def get(self, request):
        form = PurchaseOrderForm()
        context = {
            'form': form
        }
        return render(request, 'core/purchase-order.html', context=context)
    
    def post(self, request):
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            work_location_id = form.cleaned_data['work_location_id'].id
            fullname = form.cleaned_data['fullname']
            tel = form.cleaned_data['tel']
            delivery_address = form.cleaned_data['delivery_address']
            str_dudate = form.cleaned_data['delivery_date'].split(" - ")
            start_week_date = datetime.strptime(str_dudate[0] , "%m-%d-%Y")
            end_week_date = datetime.strptime(str_dudate[0] , "%m-%d-%Y")
            if len(str_dudate) > 1:
                end_week_date = datetime.strptime(str_dudate[1] , "%m-%d-%Y")
            province = form.cleaned_data['province']
            district = form.cleaned_data['district']
            amphoe = form.cleaned_data['amphoe']
            zipcode = form.cleaned_data['zipcode']
            comment = form.cleaned_data['comment']
            try:
                with transaction.atomic():
                    customer = Customer.objects.create(fullname=fullname, tel=tel)
                    order = SaleOrder.objects.create(form_date=date,customer_id=customer.id, province=province, district=district,
                    amphoe=amphoe, zipcode=zipcode, delivery_address=delivery_address,
                    delivery_start_date=start_week_date,delivery_end_date=end_week_date , work_location_id=work_location_id,
                    comment = comment)
                    order_id = order.id
                return redirect(f'/purchase-order/{order_id}/item')
            except:
                print('error create database')
        else:
            print('error invalid form')
        return redirect(f'/purchase-order/')


@method_decorator(login_required, name='dispatch')
class PurchaseOrderDetail(View):

    def get(self, request, id):
        sale_order = SaleOrder.objects.get(id=id)
        customer = Customer.objects.get(id=sale_order.customer_id)
        work_location = WorkLocation.objects.get(id=sale_order.work_location_id)
        objects = SaleOrderDetail.objects.filter(sale_order=sale_order)
        delivery_date = sale_order.delivery_start_date
        if sale_order.delivery_start_date != sale_order.delivery_end_date:
            delivery_date = sale_order.delivery_start_date.strftime("%m/%d/%Y") + ' - ' + sale_order.delivery_end_date.strftime("%m/%d/%Y")
        objects,summary_price = self.get_object_detail(objects)
        price_detail = self.get_price_detail(summary_price,sale_order)
        status = self.mapping_status(sale_order.status)
        signauter_url = EmployeeSignature.objects.get(id=sale_order.signature_id).image.url
        context = {
            'customer': customer,
            'work_location':work_location,
            'sale_order': sale_order,
            'delivery_date': delivery_date,
            'objects': objects,
            'price_detail' :  price_detail,
            'status': status,
            'signauter_url': signauter_url
        }
        return render(request, 'core/purchase-order-detail.html',context=context)

    def get_object_detail(self, objects):
        result = []
        summary_price = 0
        for item in objects:
            result.append({
                'model': ItemModel.get_object(item.model_id),
                'type': ItemType.get_object(item.type_id),
                'color': ItemColor.get_object(item.color_id),
                'material': ItemMaterial.get_object(item.material_id),
                'images': ItemImage.get_all_images(item),
                'amount': item.amount,
                'price': item.price,
                'id': item.id
            })
            summary_price += item.price
        return result,summary_price
    
    def get_price_detail(self,summary_price, sale_order):
        deposit_price = 0
        if sale_order.deposite_type == '1':
            deposit_price = sale_order.deposite_money
        elif sale_order.deposite_type == '0':
            deposit_price = summary_price * Decimal( sale_order.deposite_percent / 100)
        remain_price = summary_price - deposit_price
        result = {
                'summary_price' : summary_price,
                'deposit_price' : f'{deposit_price:.2f}',
                'remain_price' : f'{remain_price:.2f}'
        }
        return result

    def mapping_status(self,status):
        return 2


@method_decorator(login_required, name='dispatch')
class PurchaseOrderItem(View):

    def get(self, request, id):
        form = ItemForm()
        sale_order = SaleOrder.objects.filter(id=id).first()
        objects = SaleOrderDetail.objects.filter(sale_order=sale_order)
        user = request.user
        sale_form = SaleForm()
        context = {
            'form': form,
            'sale_form': sale_form,
            'objects': self.get_object_detail(objects),
            'signature': f'{user.first_name} {user.last_name}'
        }
        return render(request, 'core/purchase-order-item.html', context=context)

    def get_object_detail(self, objects):
        result = []
        for item in objects:
            result.append({
                'model': ItemModel.get_object(item.model_id),
                'type': ItemType.get_object(item.type_id),
                'color': ItemColor.get_object(item.color_id),
                'material': ItemMaterial.get_object(item.material_id),
                'images': ItemImage.get_all_images(item),
                'amount': item.amount,
                'price': item.price,
                'id': item.id
            })
        return result

    def post(self, request, id):
        form = ItemForm(request.POST, request.FILES)
        sale_form = SaleForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    model_id = form.cleaned_data['model_id'].id
                    type_id = form.cleaned_data['type_id'].id
                    color_id = form.cleaned_data['color_id'].id
                    material_id = form.cleaned_data['material_id'].id
                    price = form.cleaned_data['price']
                    amount = form.cleaned_data['amount']
                    files = request.FILES.getlist('files')
                    sale_order = SaleOrder.objects.get(id=id)
                    detail = SaleOrderDetail.objects.create(sale_order=sale_order, model_id=model_id, type_id=type_id, color_id=color_id,
                                                                material_id=material_id, price=price, amount=amount)
                    for file in files:
                        ItemImage.objects.create(image=file, order_detail=detail)
            except:
                print('error', form.errors)
        if sale_form.is_valid():
            user = request.user
            signature = EmployeeSignature.objects.get(user=user)
            sale_form.cleaned_data['deposite_percent'] = sale_form.cleaned_data['deposite_percent'] or 0
            sale_form.cleaned_data['deposite_money'] = sale_form.cleaned_data['deposite_money'] or 0
            SaleOrder.objects.update(**(sale_form.cleaned_data), status=SaleOrder.WATING_APPROVED, signature_id=signature.id)
            return redirect('/')
        else:
            print(sale_form.errors)
        return redirect(f'/purchase-order/{id}/item')


@method_decorator(login_required, name='dispatch')
class PurchaseOrderEditItem(View):

    def get_order(self, id):
        sale_order = SaleOrder.objects.get(id=id)
        customer_id = sale_order.customer_id
        customer = Customer.objects.get(id=customer_id)
        return sale_order, customer

    def get_object_detail(self, objects):
        result = []
        for item in objects:
            result.append({
                'model': ItemModel.get_object(item.model_id),
                'type': ItemType.get_object(item.type_id),
                'color': ItemColor.get_object(item.color_id),
                'material': ItemMaterial.get_object(item.material_id),
                'images': ItemImage.get_all_images(item),
                'amount': item.amount,
                'price': item.price,
                'id': item.id
            })
        return result

    def get(self, request, id):
        sale_order, customer = self.get_order(id)
        init_saleorder_form = SaleForm.initial_data(sale_order)
        sale_form = SaleForm(initial=init_saleorder_form)
        form = ItemForm()
        objects = SaleOrderDetail.objects.filter(sale_order=sale_order)
        user = request.user
        context = {
            'order_id': sale_order.id,
            'form': form,
            'sale_form': sale_form,
            'objects': self.get_object_detail(objects),
            'signature': f'{user.first_name} {user.last_name}'
        }
        return render(request, 'core/purchase-order-edit-item.html', context=context)

    def post(self, request, id):
        form = ItemForm(request.POST, request.FILES)
        sale_form = SaleForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    model_id = form.cleaned_data['model_id'].id
                    type_id = form.cleaned_data['type_id'].id
                    color_id = form.cleaned_data['color_id'].id
                    material_id = form.cleaned_data['material_id'].id
                    price = form.cleaned_data['price']
                    amount = form.cleaned_data['amount']
                    files = request.FILES.getlist('files')
                    sale_order = SaleOrder.objects.get(id=id)
                    detail = SaleOrderDetail.objects.create(sale_order=sale_order, model_id=model_id, type_id=type_id, color_id=color_id,
                                                                material_id=material_id, price=price, amount=amount)
                    for file in files:
                        ItemImage.objects.create(image=file, order_detail=detail)
            except:
                print('error', form.errors)
        if sale_form.is_valid():
            user = request.user
            signature = EmployeeSignature.objects.get(user=user)
            sale_form.cleaned_data['deposite_percent'] = sale_form.cleaned_data['deposite_percent'] or 0
            sale_form.cleaned_data['deposite_money'] = sale_form.cleaned_data['deposite_money'] or 0
            SaleOrder.objects.update(**(sale_form.cleaned_data), status=SaleOrder.WATING_APPROVED, signature_id=signature.id)
            return redirect('/')
        else:
            print(sale_form.errors)
        return redirect(f'/purchase-order/edit/{id}/item')


@method_decorator(login_required, name='dispatch')
class PurchaseOrderEdit(View):

    def get_order(self, id):
        sale_order = SaleOrder.objects.get(id=id)
        customer_id = sale_order.customer_id
        customer = Customer.objects.get(id=customer_id)
        return sale_order, customer
    
    def get(self, request, id):
        sale_order = SaleOrder.objects.get(id=id)
        customer_id = sale_order.customer_id
        customer = Customer.objects.get(id=customer_id)
        init_purchase_form = PurchaseOrderForm.initial_data(customer, sale_order)
        user_form = PurchaseOrderForm(initial=init_purchase_form)
        user = request.user
        delivery_date = sale_order.delivery_start_date
        if sale_order.delivery_start_date != sale_order.delivery_end_date:
            delivery_date = sale_order.delivery_start_date.strftime("%m/%d/%Y") + ' - ' + sale_order.delivery_end_date.strftime("%m/%d/%Y")
        context = {
            'user_form': user_form,
            'delivery_date': delivery_date,
        }
        return render(request, 'core/purchase-order-edit.html', context=context)

    def get_object_detail(self, objects):
        result = []
        for item in objects:
            result.append({
                'model': ItemModel.get_object(item.model_id),
                'type': ItemType.get_object(item.type_id),
                'color': ItemColor.get_object(item.color_id),
                'material': ItemMaterial.get_object(item.material_id),
                'images': ItemImage.get_all_images(item),
                'amount': item.amount,
                'price': item.price,
                'id': item.id
            })
        return result

    def post(self, request, id):
        sale_order, customer = self.get_order(id)
        user_form = PurchaseOrderForm(request.POST)
        if user_form.is_valid():
            fullname = user_form.cleaned_data['fullname']
            tel = user_form.cleaned_data['tel']
            try:
                with transaction.atomic():
                    Customer.objects.filter(id=customer.id).update(fullname=fullname, tel=tel)
                    self.update_sale_order(sale_order, user_form)
                    return redirect('/purchase-order/edit/1/item')
            except:
                print('write database error')
            
        return redirect('/purchase-order/edit/1')

    def update_sale_order(self, sale_order, form):
        form.cleaned_data.pop('fullname')
        form.cleaned_data.pop('tel')
        form_date = form.cleaned_data['date']
        form.cleaned_data['work_location_id'] = form.cleaned_data['work_location_id'].id
        form.cleaned_data.pop('date')
        str_dudate = form.cleaned_data['delivery_date'].split(" - ")
        start_week_date = datetime.strptime(str_dudate[0] , "%m/%d/%Y")
        end_week_date = datetime.strptime(str_dudate[0] , "%m/%d/%Y")
        if len(str_dudate) > 1:
            end_week_date = datetime.strptime(str_dudate[1] , "%m/%d/%Y")
        form.cleaned_data.pop('delivery_date')
        SaleOrder.objects.filter(id=sale_order.id).update(**(form.cleaned_data), delivery_start_date=start_week_date, 
                                delivery_end_date=end_week_date, form_date=form_date)

@method_decorator(login_required, name='dispatch')
class AdminManagement(ListView):
    template_name = 'core/admin-management.html'
    paginate_by = 1

    def get_queryset(self):
        result = []
        orders = SaleOrder.objects.filter(status=SaleOrder.WATING_APPROVED)
        for order in orders:
            result.append({
                'customer': Customer.objects.get(id=order.customer_id),
                'order': order,
            })
        return result


@method_decorator(login_required, name='dispatch')
class SaleManagement(ListView):
    template_name = 'core/sale-management.html'
    paginate_by = 10

    def get_queryset(self):
        result = []
        self.request.user
        signature = EmployeeSignature.objects.get(user=self.request.user)
        orders = SaleOrder.objects.filter(status=SaleOrder.WATING_APPROVED, signature_id=signature.id)
        for order in orders:
            result.append({
                'customer': Customer.objects.get(id=order.customer_id),
                'order': order,
            })
        return result


@method_decorator(login_required, name='dispatch')
class Management(ListView):
    template_name = 'core/management.html'
    paginate_by = 2

    def get_queryset(self):
        result = []
        month_range = self.request.GET.get('query', None)
        orders = SaleOrder.objects.filter(status=SaleOrder.ON_GOING)
        if month_range:
            start_month = datetime.strptime(month_range, '%Y-%m')
            end_month = start_month + relativedelta.relativedelta(months=1) - timedelta(days=1)
            orders = orders.filter(created_date__range=(start_month, end_month))
        for order in orders:
            result.append({
                'customer': Customer.objects.get(id=order.customer_id),
                'order': order,
                'flag': self.check_delivery_date(order.delivery_end_date),
            })
        return result
    
    def check_delivery_date(self, date):
        # 0 = nomral
        # 1 = yellow
        # 2 = red
        diff_date = date - timezone.now().date()
        if diff_date.days <= 7 and diff_date.days >= 1:
            return 1
        elif diff_date.days <= 0:
            return 2
        else:
            return 0


@method_decorator(login_required, name='dispatch')
class Summary(View):

    def get(self, request):
        return render(request, 'core/summary.html')

