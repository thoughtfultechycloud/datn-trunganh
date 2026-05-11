from django.urls import path
from . import views

urlpatterns = [
    path('update/<int:pk>/', views.update_opening_balance, name='opening_update_balance'),
]
