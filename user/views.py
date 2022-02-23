from multiprocessing import context
import pdb
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
# Create your views here.

class LoginView(View):

    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {'msg': 'เข้าสู่ระบบไม่สำเร็จ กรุณาตรวจสอบ username หรือ password อีกครั้ง'}
            return render(request, 'user/login.html', context=context)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/user/login/')

    