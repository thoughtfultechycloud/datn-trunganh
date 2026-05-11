from django.contrib import admin
from django.utils.html import format_html

from .models import SoDuDauKi


@admin.register(SoDuDauKi)
class SoDuDauKiAdmin(admin.ModelAdmin):
    change_list_template = 'opening/so_du_dau_ki_list.html'
    list_display         = ('account', 'debit_balance', 'credit_balance', 'entry_date', 'entered_by', 'hanh_dong')
    list_display_links   = None
    list_filter          = ()
    search_fields        = ('account__account_code', 'account__account_name')

    def hanh_dong(self, obj):
        return format_html(
            '<button type="button" class="btn btn-sm btn-warning" '
            'onclick="openEditBalance({}, \'{}\', \'{}\')">'
            '<i class="fas fa-edit"></i>'
            '</button>',
            obj.pk, obj.debit_balance, obj.credit_balance,
        )
    hanh_dong.short_description = 'Hành động'

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return False

    # def has_delete_permission(self, *args, **kwargs):
    #     return False
