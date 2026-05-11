from django.urls import path
from . import views

urlpatterns = [
    path('in-phieu-chi/<str:pk>/', views.in_phieu_chi, name='voucher_in_phieu_chi'),
]
