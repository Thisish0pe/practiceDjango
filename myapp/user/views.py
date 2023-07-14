from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm

# Create your views here.
### Registration
class Registration(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')

        form = RegisterForm()
        context = {
            "title": "User",
            "form": form,
        }
        return render(request, 'user/user_register.html', context)
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')
        

### Login 
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        
        form = LoginForm()
        context = {
            "title": "User",
            "form": form
        }
        return render(request, 'user/user_login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('blog:list')
        
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)

            if user:
                login(request, user)
                return redirect('blog:list')
        
        # 만약 유저가 회원이 아니라면 is_valid() 조건문에 의해 자동적으로 오류 메시지 발송됨
        context = {
            "form": form
        }
        return render(request, 'user/user_login.html', context)


### Logout
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('blog:list')
    