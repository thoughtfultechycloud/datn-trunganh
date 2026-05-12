from django.contrib import admin
from django.db.models import Sum

from .models import GiayBaoCo, GiayBaoNo, Invoice, InvoiceLineItem, PhieuChi, PhieuThu


class InvoiceLineItemInline(admin.TabularInline):
    model         = InvoiceLineItem
    extra         = 1
    fields        = ('item_name', 'amount')


def vnd(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return value


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    change_form_template = 'voucher/invoice_change_form.html'
    list_display  = ('invoice_number', 'invoice_date', 'partner', 'project', 'display_total_amount', 'vat_10', 'display_vat_amount')
    list_filter   = ('project', 'vat_10')
    search_fields = ('invoice_number', 'partner__partner_name', 'tax_code')
    readonly_fields = ('display_total_amount', 'display_vat_amount')
    inlines       = [InvoiceLineItemInline]
    fieldsets = (
        ('Thông tin phiếu', {
            'fields': (
                'invoice_number', 'invoice_date', 'project',
                'seller_unit', 'seller_address', 'reason',
                'partner', 'debit_account', 'credit_account', 'display_total_amount',
            ),
        }),
        ('Giá trị gia tăng 10%', {
            'fields': ('vat_10', 'vat_debit_account', 'vat_credit_account', 'display_vat_amount'),
        }),
    )

    @admin.display(description='Tổng tiền')
    def display_total_amount(self, obj):
        return vnd(obj.total_amount)

    @admin.display(description='Tiền thuế GTGT (10%)')
    def display_vat_amount(self, obj):
        return vnd(obj.vat_amount)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        invoice = form.instance
        total = invoice.line_items.aggregate(s=Sum('amount'))['s'] or 0
        Invoice.objects.filter(pk=invoice.pk).update(total_amount=total)


class BaseVoucherAdmin(admin.ModelAdmin):
    list_display  = ('voucher_number', 'voucher_date', 'partner', 'project', 'display_amount', 'created_by')
    list_filter   = ('project',)
    search_fields = ('voucher_number', 'partner__partner_name', 'reason', 'created_by')
    exclude       = ('voucher_type',)

    @admin.display(description='Số tiền (VNĐ)')
    def display_amount(self, obj):
        return vnd(obj.amount)

    def save_model(self, request, obj, form, change):
        obj.voucher_type = self._voucher_type
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(voucher_type=self._voucher_type)


@admin.register(PhieuThu)
class PhieuThuAdmin(BaseVoucherAdmin):
    _voucher_type        = 'PT'
    change_form_template = 'voucher/phieuthu_change_form.html'


@admin.register(PhieuChi)
class PhieuChiAdmin(BaseVoucherAdmin):
    _voucher_type        = 'PC'
    change_form_template = 'voucher/phieuchi_change_form.html'


class BaseBankNoticeAdmin(admin.ModelAdmin):
    list_display  = ('notice_number', 'notice_date', 'partner', 'project', 'display_amount', 'exchange_rate', 'from_bank_account', 'to_bank_account')
    list_filter   = ('project',)
    search_fields = ('notice_number', 'partner__partner_name', 'description', 'to_bank_account')
    exclude       = ('notice_type',)

    @admin.display(description='Số tiền')
    def display_amount(self, obj):
        return vnd(obj.amount)

    def save_model(self, request, obj, form, change):
        obj.notice_type = self._notice_type
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(notice_type=self._notice_type)


@admin.register(GiayBaoNo)
class GiayBaoNoAdmin(BaseBankNoticeAdmin):
    _notice_type         = 'GBN'
    change_form_template = 'voucher/giaybaono_change_form.html'


@admin.register(GiayBaoCo)
class GiayBaoCoAdmin(BaseBankNoticeAdmin):
    _notice_type         = 'GBC'
    change_form_template = 'voucher/giaybaoco_change_form.html'
