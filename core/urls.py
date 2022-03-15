from django.urls import path
from core.views import HomePage, PurchaseOrder, AdminManagement, Management, Summary
from core.views import PurchaseOrderDetail, PurchaseOrderEdit, PurchaseOrderItem, SaleManagement, PurchaseOrderEditItem
from core.api.v1 import AdminManagementAPI, ExportExcelAPI, ManagementAPI, DepartmentListAPI, PurchaseOrdertAPI

urlpatterns = [
    path('', HomePage.as_view()),
    path('purchase-order/', PurchaseOrder.as_view()),
    path('purchase-order/<int:id>', PurchaseOrderDetail.as_view()),
    path('purchase-order/<int:id>/item', PurchaseOrderItem.as_view(), name='purchase-order-item'),
    path('purchase-order/edit/<int:id>', PurchaseOrderEdit.as_view()),
    path('purchase-order/edit/<int:id>/item', PurchaseOrderEditItem.as_view()),
    path('admin-management/', AdminManagement.as_view()),
    path('sale-management/', SaleManagement.as_view()),
    path('management/', Management.as_view()),
    path('summary/', Summary.as_view()),

    # api
    path('api/admin-management', AdminManagementAPI.as_view()),
    path('api/purchase-order', PurchaseOrdertAPI.as_view()),
    path('api/management', ManagementAPI.as_view()),
    path('api/department', DepartmentListAPI.as_view()),
    path('api/export-excel', ExportExcelAPI.as_view()),
    
]

# api url
urlpatterns += [
]