from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import DebtReport


@admin.register(DebtReport)
class DebtReportAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('report_debt'))

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
