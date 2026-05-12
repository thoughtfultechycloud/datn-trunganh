from django.contrib import admin
from django.shortcuts import render

from .models import BaoCaoNoPT, BaoCaoNoPTra, BangKeChiTien
from .views import get_bao_cao_no_context, get_bang_ke_chi_tien_context


class BaseReportAdmin(admin.ModelAdmin):
    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def _render(self, request, template, extra_context=None):
        ctx = {
            **self.admin_site.each_context(request),
            'opts':  self.model._meta,
            'title': self.model._meta.verbose_name,
        }
        if extra_context:
            ctx.update(extra_context)
        return render(request, template, ctx)


@admin.register(BaoCaoNoPT)
class BaoCaoNoPTAdmin(BaseReportAdmin):
    def changelist_view(self, request, extra_context=None):
        return self._render(request, 'report/bao_cao_no_pt.html', get_bao_cao_no_context(request))


@admin.register(BaoCaoNoPTra)
class BaoCaoNoPTraAdmin(BaseReportAdmin):
    def changelist_view(self, request, extra_context=None):
        return self._render(request, 'report/bao_cao_no_ptra.html', get_bao_cao_no_context(request))


@admin.register(BangKeChiTien)
class BangKeChiTienAdmin(BaseReportAdmin):
    def changelist_view(self, request, extra_context=None):
        return self._render(request, 'report/bang_ke_chi_tien.html', get_bang_ke_chi_tien_context(request))
