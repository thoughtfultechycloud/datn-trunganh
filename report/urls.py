from django.urls import path
from . import views

urlpatterns = [
    path('no-phai-thu/',  views.bao_cao_no_pt,   name='report_no_pt'),
    path('no-phai-tra/',  views.bao_cao_no_ptra,  name='report_no_ptra'),
]
