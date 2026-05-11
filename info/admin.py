from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import HDSD, TTCongTy


class BaseInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TTCongTy)
class TTCongTyAdmin(BaseInfoAdmin):
    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('info_cong_ty'))


@admin.register(HDSD)
class HDSDAdmin(BaseInfoAdmin):
    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('info_hdsd'))
