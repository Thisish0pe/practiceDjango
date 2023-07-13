from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm

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
        form = RegisterForm(request)
        if form.is_valid():
            form.save()
            return redirect('user:log')