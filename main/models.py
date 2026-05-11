from django.contrib.auth.models import User
from django.db import models


class AccountCategory(models.Model):
    account_code = models.CharField(max_length=10, primary_key=True, verbose_name='Mã TK')
    account_name = models.CharField(max_length=150, verbose_name='Tên tài khoản')
    parent       = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
        verbose_name='TK cấp trên',
    )
    is_active    = models.BooleanField(default=True, verbose_name='Đang sử dụng')

    class Meta:
        verbose_name        = 'Tài khoản kế toán'
        verbose_name_plural = 'Tài khoản kế toán'

    def __str__(self):
        return f'{self.account_code} — {self.account_name}'


class Partner(models.Model):
    TYPE_CHOICES = [
        ('KH',  'Khách hàng'),
        ('NCC', 'Nhà cung cấp'),
    ]

    partner_code    = models.CharField(max_length=10, primary_key=True, verbose_name='Mã đối tác')
    partner_name    = models.CharField(max_length=150, verbose_name='Tên đối tác')
    partner_type    = models.CharField(max_length=5, choices=TYPE_CHOICES, verbose_name='Loại đối tác')
    address         = models.CharField(max_length=200, blank=True, verbose_name='Địa chỉ')
    tax_code        = models.CharField(max_length=15, blank=True, verbose_name='Mã số thuế')
    email           = models.EmailField(max_length=100, blank=True, verbose_name='Email')
    phone           = models.CharField(max_length=20, blank=True, verbose_name='Điện thoại')
    representative  = models.CharField(max_length=100, blank=True, verbose_name='Người đại diện')
    debt_limit      = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Hạn mức công nợ (VNĐ)')
    is_active       = models.BooleanField(default=True, verbose_name='Hoạt động')

    class Meta:
        verbose_name        = 'Đối tác'
        verbose_name_plural = 'Đối tác'

    def __str__(self):
        return f'{self.partner_code} — {self.partner_name}'


class Bank(models.Model):
    bank_code   = models.CharField(max_length=10, primary_key=True, verbose_name='Mã ngân hàng')
    bank_name   = models.CharField(max_length=100, verbose_name='Tên ngân hàng')
    branch      = models.CharField(max_length=100, blank=True, verbose_name='Chi nhánh')
    address     = models.CharField(max_length=200, blank=True, verbose_name='Địa chỉ')
    is_active   = models.BooleanField(default=True, verbose_name='Hoạt động')

    class Meta:
        verbose_name        = 'Ngân hàng'
        verbose_name_plural = 'Ngân hàng'

    def __str__(self):
        return f'{self.bank_code} — {self.bank_name}'


class CompanyBankAccount(models.Model):
    CURRENCY_CHOICES = [
        ('VND', 'VND'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]

    account_number  = models.CharField(max_length=20, primary_key=True, verbose_name='Số tài khoản')
    account_holder  = models.CharField(max_length=150, verbose_name='Chủ tài khoản')
    bank            = models.ForeignKey(Bank, on_delete=models.PROTECT, verbose_name='Ngân hàng')
    currency        = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='VND', verbose_name='Loại tiền')
    balance         = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Số dư tham chiếu')
    is_active       = models.BooleanField(default=True, verbose_name='Còn hiệu lực')

    class Meta:
        verbose_name        = 'Tài khoản ngân hàng'
        verbose_name_plural = 'Tài khoản ngân hàng công ty'

    def __str__(self):
        return f'{self.account_number} — {self.account_holder}'


class Project(models.Model):
    project_code   = models.CharField(max_length=10, primary_key=True, verbose_name='Mã dự án')
    project_name   = models.CharField(max_length=200, verbose_name='Tên dự án')
    investor       = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Chủ đầu tư')
    start_date     = models.DateField(verbose_name='Ngày khởi công')
    end_date       = models.DateField(null=True, blank=True, verbose_name='Ngày hoàn thành dự kiến')
    contract_value = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Giá trị hợp đồng (VNĐ)')
    location       = models.CharField(max_length=200, blank=True, verbose_name='Địa chỉ')
    manager        = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Trưởng dự án')

    class Meta:
        verbose_name        = 'Dự án'
        verbose_name_plural = 'Dự án'

    def __str__(self):
        return f'{self.project_code} — {self.project_name}'




class PartnerOpeningBalance(models.Model):
    partner         = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Đối tác')
    account         = models.ForeignKey(AccountCategory, on_delete=models.PROTECT, verbose_name='Tài khoản (131/331)')
    project         = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Dự án')
    period          = models.CharField(max_length=10, verbose_name='Kỳ kế toán (VD: 2024-01)')
    debit_balance   = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Số dư Nợ đầu kỳ')
    credit_balance  = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Số dư Có đầu kỳ')
    entry_date      = models.DateField(auto_now_add=True, verbose_name='Ngày nhập số liệu')
    entered_by      = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Người nhập liệu')

    class Meta:
        verbose_name        = 'Số dư nợ công nợ đầu kỳ'
        verbose_name_plural = 'Số dư nợ công nợ đầu kỳ'
        unique_together     = [('partner', 'account', 'project', 'period')]

    def __str__(self):
        return f'{self.partner_id} / {self.account_id} / {self.period}'


class AccountOpeningBalance(models.Model):
    account        = models.ForeignKey(AccountCategory, on_delete=models.PROTECT, unique=True, verbose_name='Tài khoản kế toán')
    debit_balance  = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Số dư Nợ đầu kỳ')
    credit_balance = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Số dư Có đầu kỳ')
    entry_date     = models.DateField(auto_now_add=True, verbose_name='Ngày nhập số liệu')
    entered_by     = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Người nhập liệu')

    class Meta:
        verbose_name        = 'Số dư đầu kỳ tài khoản tổng hợp'
        verbose_name_plural = 'Số dư đầu kỳ tài khoản tổng hợp'

    def __str__(self):
        return str(self.account_id)
