from django.contrib import admin
from django.shortcuts import render
from django.urls import reverse

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
        request.GET = request.GET.copy()
        request.GET['account'] = '131'
        ctx = get_bao_cao_no_context(request)
        ctx['export_url'] = reverse('report_xuat_no_pt')
        return self._render(request, 'report/bao_cao_no_pt.html', ctx)


@admin.register(BaoCaoNoPTra)
class BaoCaoNoPTraAdmin(BaseReportAdmin):
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        request.GET['account'] = '331'
        ctx = get_bao_cao_no_context(request)
        ctx['export_url'] = reverse('report_xuat_no_ptra')
        return self._render(request, 'report/bao_cao_no_ptra.html', ctx)


@admin.register(BangKeChiTien)
class BangKeChiTienAdmin(BaseReportAdmin):
    def changelist_view(self, request, extra_context=None):
        return self._render(request, 'report/bang_ke_chi_tien.html', get_bang_ke_chi_tien_context(request))
