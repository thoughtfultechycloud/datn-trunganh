from django.urls import path
from . import views

urlpatterns = [
    path('so-cai/',           views.so_cai_tk,           name='ledger_so_cai'),
    path('so-cai/xuat/',      views.xuat_so_cai_tk,      name='ledger_xuat_so_cai'),
    path('so-chi-tiet/',      views.so_chi_tiet_tk,      name='ledger_so_chi_tiet'),
    path('so-chi-tiet/xuat/', views.xuat_so_chi_tiet_tk, name='ledger_xuat_so_chi_tiet'),
]
