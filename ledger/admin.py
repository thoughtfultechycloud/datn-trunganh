from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import SoCaiTK, SoChiTietTK


class BaseledgerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SoCaiTK)
class SoCaiTKAdmin(BaseledgerAdmin):
    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('ledger_so_cai'))


@admin.register(SoChiTietTK)
class SoChiTietTKAdmin(BaseledgerAdmin):
    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('ledger_so_chi_tiet'))
