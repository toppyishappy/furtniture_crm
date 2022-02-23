from datetime import datetime
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator([login_required, csrf_exempt], name='dispatch')
class PurchaseOrderAPI(View):
    
    def post(self, request):
        print(request.body)
        return JsonResponse({})
