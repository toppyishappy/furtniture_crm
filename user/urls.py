from django.urls import path
from user.views import LoginView

urlpatterns = [
    path('', LoginView.as_view()),
]