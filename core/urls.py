"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core.views import dashboard

admin.site.site_header = "AIBox - Quản lí chi phí dự án"
admin.site.site_title = "AIBox - Quản lí chi phí dự án"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('dashboard/', dashboard, name='dashboard'),
    path('opening/', include('opening.urls')),
    path('voucher/', include('voucher.urls')),
    path('report/', include('report.urls')),
    path('ledger/', include('ledger.urls')),
    path('info/',   include('info.urls')),
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
]
