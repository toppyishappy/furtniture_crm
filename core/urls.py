from django.urls import path
from core.views import HomePage, PurchaseOrder

urlpatterns = [
    path('', HomePage.as_view()),
    path('purchase-order/', PurchaseOrder.as_view()),
]

# api url
urlpatterns += [
]