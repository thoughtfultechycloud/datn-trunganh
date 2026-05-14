from django.urls import path
from . import views

urlpatterns = [
    path('no-phai-thu/',          views.bao_cao_no_pt,          name='report_no_pt'),
    path('no-phai-thu/xuat/',     views.xuat_bao_cao_no_pt,     name='report_xuat_no_pt'),
    path('no-phai-tra/',          views.bao_cao_no_ptra,         name='report_no_ptra'),
    path('no-phai-tra/xuat/',     views.xuat_bao_cao_no_ptra,    name='report_xuat_no_ptra'),
    path('bang-ke-chi-tien/xuat/', views.xuat_bang_ke_chi_tien, name='report_xuat_bang_ke_chi_tien'),
]
