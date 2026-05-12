from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from .models import AccountCategory, Partner, PartnerOpeningBalance, Bank, CompanyBankAccount, Project

def _user_str(self):
    full_name = self.get_full_name()
    return f'{self.username} - {full_name}' if full_name else self.username

User.__str__ = _user_str

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = None

@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    ordering = None


@admin.register(AccountCategory)
class AccountCategoryAdmin(admin.ModelAdmin):
    list_display  = ('account_code', 'account_name', 'parent', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('account_code', 'account_name')
    list_editable = ('is_active',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display  = ('partner_code', 'partner_name', 'partner_type', 'phone', 'email', 'debt_limit', 'is_active')
    list_filter   = ('partner_type', 'is_active')
    search_fields = ('partner_code', 'partner_name', 'tax_code', 'email', 'phone')
    list_editable = ('is_active',)
    radio_fields  = {'partner_type': admin.HORIZONTAL}


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display  = ('bank_code', 'bank_name', 'branch', 'address', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('bank_code', 'bank_name', 'branch')
    list_editable = ('is_active',)


@admin.register(CompanyBankAccount)
class CompanyBankAccountAdmin(admin.ModelAdmin):
    list_display  = ('account_number', 'account_holder', 'bank', 'currency', 'balance', 'is_active')
    list_filter   = ('currency', 'is_active', 'bank')
    search_fields = ('account_number', 'account_holder')
    list_editable = ('is_active',)
    radio_fields  = {'currency': admin.HORIZONTAL}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('project_code', 'project_name', 'investor', 'manager', 'start_date', 'end_date', 'contract_value')
    list_filter   = ('investor',)
    search_fields = ('project_code', 'project_name', 'location')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'manager':
            kwargs['queryset'] = User.objects.filter(groups__name='Trưởng dự án').distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)





