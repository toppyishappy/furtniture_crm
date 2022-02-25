from datetime import datetime
import json

from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from core.models import Department, SaleOrder, SaleOrderDetail
from log.models import DepartmentLog

@method_decorator([login_required, csrf_exempt], name='dispatch')
class AdminManagementAPI(View):
    
    def post(self, request):
        data = json.loads(request.body)
        order_id = data['order_id']
        order = SaleOrder.objects.filter(id=order_id).first()
        order.status = SaleOrder.ON_GOING
        order.save()
        return JsonResponse({'ok': True})


@method_decorator([login_required, csrf_exempt], name='dispatch')
class PurchaseOrdertAPI(View):
    
    def delete(self, request):
        data = json.loads(request.body)
        item_id = data['item_id']
        SaleOrderDetail.objects.filter(id=item_id).delete()
        return JsonResponse({'ok': True})

@method_decorator([login_required, csrf_exempt], name='dispatch')
class DepartmentListAPI(View):
    
    def get(self, request):
        result = []
        order_id = request.GET['order_id']
        departments = Department.objects.filter(status=True)
        for department in departments:
            # risk bug multi departmentlog
            log = DepartmentLog.objects.filter(department_id=department.id, order__id=order_id, status=True).first()
            result.append({
                'id': department.id,
                'name': department.name,
                'flag': self.check_flag(log),
            })
        return JsonResponse({'ok': True, 'departments': result})

    def check_flag(self, log):
        # 0 = init, 1 = start, 2 = stop, 3 = done
        if not log:
            return 0
        elif log.start_time and log.end_time:
            return 3
        elif log.end_time:
            return 2
        elif log.start_time:
            return 1
        else:
            return 0

@method_decorator([login_required, csrf_exempt], name='dispatch')
class ManagementAPI(View):
    
    def post(self, request):
        now = timezone.now()
        data = json.loads(request.body)
        action = data['action']
        department_id = data['department_id']
        order_id = data['order_id']
        order = SaleOrder.objects.filter(id=order_id).first()
        log = DepartmentLog.objects.filter(order=order, department_id=department_id, status=True).first()
        if not log:
            log = DepartmentLog(order=order, department_id=department_id)
        if action == 'start':
            log.start_time = now
        elif action == 'stop':
            log.end_time = now
        elif action == 'reject':
            log.status = False
        log.save()

        return JsonResponse({'ok': True})
