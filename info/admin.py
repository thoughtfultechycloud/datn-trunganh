from django.contrib import admin
from django.shortcuts import render

from .models import HDSD, TTCongTy


class BaseInfoAdmin(admin.ModelAdmin):
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


@admin.register(TTCongTy)
class TTCongTyAdmin(BaseInfoAdmin):
    def changelist_view(self, request, extra_context=None):
        return self._render(request, 'info/tt_cong_ty.html', extra_context)


@admin.register(HDSD)
class HDSDAdmin(BaseInfoAdmin):
    def changelist_view(self, request, extra_context=None):
        return self._render(request, 'info/hdsd.html', extra_context)
