from datetime import datetime
import io
import json
from os import stat
from user.models import Customer
import xlsxwriter

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from core.models import Department, ItemColor, ItemMaterial, ItemModel, ItemType, SaleOrder, SaleOrderDetail
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
class ExportExcelAPI(View):
    
    def get(self, request):
        id_list = request.GET.get('id_list').split(',')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        text_wrap_format = workbook.add_format({'text_wrap': 'true'})
        today = datetime.strftime(timezone.now(), '%Y-%m-%d')
        worksheet.write(0, 0, today)
        worksheet.write(1, 0, 'หมายเลข PO')
        worksheet.write(1, 1, 'แบบ')
        worksheet.write(1, 2, 'วัสดุ')
        worksheet.write(1, 3, 'สี')
        worksheet.write(1, 4, 'ประเภท')
        worksheet.write(1, 5, 'จำนวน')
        worksheet.write(1, 6, 'หมายเหตุ')
        worksheet.write(1, 7, 'ลูกค้า')
        row = 2
        for id in id_list:
            sale_order = SaleOrder.objects.filter(id=id).first()
            order_details = SaleOrderDetail.objects.filter(sale_order=sale_order)
            order_detail_length = order_details.count()
            worksheet.merge_range(row, 0, row+order_detail_length, 0, sale_order.custom_po or sale_order.id)
            worksheet.merge_range(row, 6, row+order_detail_length, 6, sale_order.comment, text_wrap_format)
            worksheet.merge_range(row, 7, row+order_detail_length, 7, Customer.objects.get(id=sale_order.customer_id).fullname)
            for detail in order_details:
                worksheet.write(row, 1, ItemModel.get_object(detail.model_id).name)
                worksheet.write(row, 2, ItemMaterial.get_object(detail.material_id).name)
                worksheet.write(row, 3, ItemColor.get_object(detail.color_id).name)
                worksheet.write(row, 4, ItemType.get_object(detail.type_id).name)
                worksheet.write(row, 5, detail.amount)
                row += 1
            row += 1
        workbook.close()

        # Rewind the buffer.
        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        filename = f'{today}_excel.xlsx'
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        # Set up the Http response.

        return response

@method_decorator([login_required, csrf_exempt], name='dispatch')
class PurchaseOrdertAPI(View):
    
    def delete(self, request):
        data = json.loads(request.body)
        item_id = data['item_id']
        SaleOrderDetail.objects.filter(id=item_id).delete()
        return JsonResponse({'ok': True})
    
    def patch(self, request):
        data = json.loads(request.body)
        item_id = data['item_id']
        status = data['status']
        SaleOrder.objects.filter(id=item_id).update(status = status)
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
