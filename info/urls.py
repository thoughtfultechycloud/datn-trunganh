from django.urls import path
from . import views

urlpatterns = [
    path('cong-ty/', views.tt_cong_ty, name='info_cong_ty'),
    path('hdsd/',    views.hdsd,        name='info_hdsd'),
]
