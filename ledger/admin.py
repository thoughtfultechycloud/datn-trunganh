from django.contrib import admin
from django.shortcuts import render

from .models import SoCaiTK, SoChiTietTK


class BaseledgerAdmin(admin.ModelAdmin):
    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def _render(self, request, template, extra_context=None):
        ctx = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': self.model._meta.verbose_name,
        }
        if extra_context:
            ctx.update(extra_context)
        return render(request, template, ctx)


@admin.register(SoCaiTK)
class SoCaiTKAdmin(BaseledgerAdmin):
    def changelist_view(self, request, extra_context=None):
        from .views import get_so_cai_context
        return self._render(request, 'ledger/so_cai_tk.html', get_so_cai_context(request))


@admin.register(SoChiTietTK)
class SoChiTietTKAdmin(BaseledgerAdmin):
    def changelist_view(self, request, extra_context=None):
        from .views import get_so_chi_tiet_context
        return self._render(request, 'ledger/so_chi_tiet_tk.html', get_so_chi_tiet_context(request))
