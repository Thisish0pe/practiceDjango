from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    #회원가입
    path('register/',views.Registration.as_view(), name='register'),
]