from django.contrib import admin

from .models import GiayBaoCo, GiayBaoNo, Invoice, PhieuChi, PhieuThu


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display  = ('invoice_number', 'invoice_date', 'partner', 'project', 'total_amount')
    list_filter   = ('project',)
    search_fields = ('invoice_number', 'partner__partner_name')


class BaseVoucherAdmin(admin.ModelAdmin):
    list_display  = ('voucher_number', 'voucher_date', 'partner', 'project', 'amount', 'created_by')
    list_filter   = ('project',)
    search_fields = ('voucher_number', 'partner__partner_name', 'reason', 'created_by')
    exclude       = ('voucher_type',)

    def save_model(self, request, obj, form, change):
        obj.voucher_type = self._voucher_type
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(voucher_type=self._voucher_type)


@admin.register(PhieuThu)
class PhieuThuAdmin(BaseVoucherAdmin):
    _voucher_type = 'PT'


@admin.register(PhieuChi)
class PhieuChiAdmin(BaseVoucherAdmin):
    _voucher_type        = 'PC'
    change_form_template = 'voucher/phieuchi_change_form.html'


class BaseBankNoticeAdmin(admin.ModelAdmin):
    list_display  = ('notice_number', 'notice_date', 'partner', 'project', 'amount', 'exchange_rate', 'from_bank_account', 'to_bank_account')
    list_filter   = ('project',)
    search_fields = ('notice_number', 'partner__partner_name', 'description', 'to_bank_account')
    exclude       = ('notice_type',)

    def save_model(self, request, obj, form, change):
        obj.notice_type = self._notice_type
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(notice_type=self._notice_type)


@admin.register(GiayBaoNo)
class GiayBaoNoAdmin(BaseBankNoticeAdmin):
    _notice_type = 'GBN'


@admin.register(GiayBaoCo)
class GiayBaoCoAdmin(BaseBankNoticeAdmin):
    _notice_type = 'GBC'
