from django.contrib import admin
from django.contrib.auth.models import User
from .models import AccountCategory, AccountOpeningBalance, Partner, PartnerOpeningBalance, Bank, CompanyBankAccount, Project, CostCategory


@admin.register(AccountCategory)
class AccountCategoryAdmin(admin.ModelAdmin):
    list_display  = ('account_code', 'account_name', 'parent', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('account_code', 'account_name')
    list_editable = ('is_active',)
    ordering      = ('account_code',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display  = ('partner_code', 'partner_name', 'partner_type', 'phone', 'email', 'debt_limit', 'is_active')
    list_filter   = ('partner_type', 'is_active')
    search_fields = ('partner_code', 'partner_name', 'tax_code', 'email', 'phone')
    list_editable = ('is_active',)
    ordering      = ('partner_code',)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display  = ('bank_code', 'bank_name', 'branch', 'address', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('bank_code', 'bank_name', 'branch')
    list_editable = ('is_active',)
    ordering      = ('bank_code',)


@admin.register(CompanyBankAccount)
class CompanyBankAccountAdmin(admin.ModelAdmin):
    list_display  = ('account_number', 'account_holder', 'bank', 'currency', 'balance', 'is_active')
    list_filter   = ('currency', 'is_active', 'bank')
    search_fields = ('account_number', 'account_holder')
    list_editable = ('is_active',)
    ordering      = ('account_number',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('project_code', 'project_name', 'investor', 'manager', 'start_date', 'end_date', 'contract_value', 'status')
    list_filter   = ('status', 'investor')
    search_fields = ('project_code', 'project_name', 'location')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'manager':
            kwargs['queryset'] = User.objects.filter(groups__name='Trưởng dự án').distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CostCategory)
class CostCategoryAdmin(admin.ModelAdmin):
    list_display  = ('category_code', 'category_name', 'project', 'cost_type', 'order')
    list_filter   = ('cost_type', 'project')
    search_fields = ('category_code', 'category_name')
    ordering      = ('project', 'order', 'category_code')


@admin.register(PartnerOpeningBalance)
class PartnerOpeningBalanceAdmin(admin.ModelAdmin):
    list_display  = ('partner', 'account', 'project', 'period', 'debit_balance', 'credit_balance', 'entry_date', 'entered_by')
    list_filter   = ('period', 'project', 'account')
    search_fields = ('partner__partner_name', 'account__account_code', 'period')
    ordering      = ('period', 'partner')
    readonly_fields = ('entry_date',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'entered_by':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(AccountOpeningBalance)
class AccountOpeningBalanceAdmin(admin.ModelAdmin):
    list_display  = ('account', 'period', 'debit_balance', 'credit_balance', 'entry_date', 'entered_by')
    list_filter   = ('period',)
    search_fields = ('account__account_code', 'account__account_name', 'period')
    ordering      = ('period', 'account')
    readonly_fields = ('entry_date',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'entered_by':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
