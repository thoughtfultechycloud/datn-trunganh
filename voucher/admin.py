from django.contrib import admin

from .models import AcceptanceRecord, BankNotice, Contract, Invoice, InvoiceLineItem, PaymentSchedule, Voucher, VoucherLineItem


class PaymentScheduleInline(admin.TabularInline):
    model  = PaymentSchedule
    extra  = 1
    fields = ('order', 'description', 'completion_pct', 'amount', 'due_date', 'actual_date', 'status')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display  = ('contract_number', 'contract_type', 'partner', 'project', 'sign_date', 'effective_date', 'expiry_date', 'contract_value', 'status')
    list_filter   = ('contract_type', 'status', 'project')
    search_fields = ('contract_number', 'partner__partner_name', 'project__project_name')
    ordering      = ('-sign_date',)
    inlines       = [PaymentScheduleInline]


@admin.register(AcceptanceRecord)
class AcceptanceRecordAdmin(admin.ModelAdmin):
    list_display  = ('record_number', 'contract', 'cost_category', 'acceptance_date', 'acceptance_value', 'completion_pct', 'status')
    list_filter   = ('status', 'cost_category__project')
    search_fields = ('record_number', 'contract__contract_number', 'signer_a', 'signer_b')
    ordering      = ('-acceptance_date',)


class InvoiceLineItemInline(admin.TabularInline):
    model           = InvoiceLineItem
    extra           = 1
    readonly_fields = ('amount',)
    fields          = ('item_name', 'unit', 'quantity', 'unit_price', 'tax_rate', 'amount', 'cost_category')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display    = ('invoice_number', 'invoice_type', 'invoice_date', 'partner', 'project', 'pre_tax_amount', 'tax_rate', 'tax_amount', 'total_amount', 'status')
    list_filter     = ('invoice_type', 'status', 'project')
    search_fields   = ('invoice_number', 'partner__partner_name')
    ordering        = ('-invoice_date',)
    readonly_fields = ('tax_amount', 'total_amount')
    inlines         = [InvoiceLineItemInline]


class VoucherLineItemInline(admin.TabularInline):
    model  = VoucherLineItem
    extra  = 1
    fields = ('cost_category', 'amount', 'description')


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display  = ('voucher_number', 'voucher_type', 'voucher_date', 'partner', 'project', 'amount', 'payment_method', 'status', 'approved_by')
    list_filter   = ('voucher_type', 'status', 'payment_method', 'project')
    search_fields = ('voucher_number', 'partner__partner_name', 'reason')
    ordering      = ('-voucher_date',)
    readonly_fields = ('approved_at',)
    inlines       = [VoucherLineItemInline]


@admin.register(BankNotice)
class BankNoticeAdmin(admin.ModelAdmin):
    list_display  = ('notice_number', 'notice_type', 'notice_date', 'partner', 'project', 'amount', 'exchange_rate', 'from_bank_account', 'to_bank_account')
    list_filter   = ('notice_type', 'project')
    search_fields = ('notice_number', 'partner__partner_name', 'description', 'to_bank_account')
    ordering      = ('-notice_date',)
