from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.Index.as_view(), name='list'),
    path("write/", views.Write.as_view(), name='write'),
    path("detail/<int:pk>/edit/", views.Updat.as_view(), name='edit'),
]