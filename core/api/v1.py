from datetime import datetime
import json

from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.models import SaleOrder

@method_decorator([login_required, csrf_exempt], name='dispatch')
class AdminManagementAPI(View):
    
    def post(self, request):
        data = json.loads(request.body)
        order_id = data['order_id']
        order = SaleOrder.objects.filter(id=order_id).first()
        order.status = SaleOrder.ON_GOING
        order.save()
        return JsonResponse({'ok': True})
