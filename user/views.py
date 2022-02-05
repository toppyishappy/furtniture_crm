from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import authenticate, login
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
            # Redirect to a success page.
            
        else:
            # Return an 'invalid login' error message.
            return redirect('/user/')

    