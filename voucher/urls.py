from django.urls import path
from . import views

urlpatterns = [
    path('in-phieu-chi/<str:pk>/',      views.in_phieu_chi,      name='voucher_in_phieu_chi'),
    path('in-phieu-thu/<str:pk>/',      views.in_phieu_thu,      name='voucher_in_phieu_thu'),
    path('in-phieu-mua-hang/<str:pk>/', views.in_phieu_mua_hang, name='voucher_in_phieu_mua_hang'),
    path('in-giay-bao-no/<str:pk>/',    views.in_giay_bao_no,    name='voucher_in_giay_bao_no'),
    path('in-giay-bao-co/<str:pk>/',    views.in_giay_bao_co,    name='voucher_in_giay_bao_co'),
]
