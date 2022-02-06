from django.urls import path
from core.views import HomePage, PurchaseOrder, AdminManagement, Management, Summary

urlpatterns = [
    path('', HomePage.as_view()),
    path('purchase-order/', PurchaseOrder.as_view()),
    path('admin-management/', AdminManagement.as_view()),
    path('management/', Management.as_view()),
    path('summary/', Summary.as_view()),
]

# api url
urlpatterns += [
]