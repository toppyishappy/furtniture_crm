from django.urls import path
from core.views import HomePage, PurchaseOrder, AdminManagement, Management, Summary, PurchaseOrderDetail, PurchaseOrderEdit, PurchaseOrderItem
from core.api.v1 import AdminManagementAPI

urlpatterns = [
    path('', HomePage.as_view()),
    path('purchase-order/', PurchaseOrder.as_view()),
    path('purchase-order/<int:id>', PurchaseOrderDetail.as_view()),
    path('purchase-order/<int:id>/item', PurchaseOrderItem.as_view()),
    path('purchase-order/edit/<int:id>', PurchaseOrderEdit.as_view()),
    path('admin-management/', AdminManagement.as_view()),
    path('management/', Management.as_view()),
    path('summary/', Summary.as_view()),

    # api
    path('api/admin-management', AdminManagementAPI.as_view()),
]

# api url
urlpatterns += [
]