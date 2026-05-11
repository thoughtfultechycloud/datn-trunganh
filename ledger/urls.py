from django.urls import path
from . import views

urlpatterns = [
    path('so-cai/',     views.so_cai_tk,     name='ledger_so_cai'),
    path('so-chi-tiet/', views.so_chi_tiet_tk, name='ledger_so_chi_tiet'),
]
