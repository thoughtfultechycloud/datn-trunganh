from django.urls import path
from . import views

urlpatterns = [
    path('debt/', views.debt_report, name='report_debt'),
]
