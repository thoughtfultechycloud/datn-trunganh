from django.db import models

from main.models import AccountCategory, CompanyBankAccount, Partner, Project




class Invoice(models.Model):
    invoice_number  = models.CharField(max_length=20, primary_key=True, verbose_name='Số hóa đơn GTGT')
    invoice_date    = models.DateField(verbose_name='Ngày lập hóa đơn')
    partner         = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Nhà cung cấp')
    tax_code        = models.CharField(max_length=20, blank=True, verbose_name='Mã số thuế')
    address         = models.CharField(max_length=300, blank=True, verbose_name='Địa chỉ')
    contact_person  = models.CharField(max_length=100, blank=True, verbose_name='Người giao dịch')
    description     = models.CharField(max_length=300, blank=True, verbose_name='Nội dung')
    project         = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Dự án')
    total_amount    = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Tổng tiền')
    debit_account       = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='debit_invoices',     verbose_name='TK Nợ (tổng tiền hàng)')
    credit_account      = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='credit_invoices',    verbose_name='TK Có (tổng tiền hàng)')
    vat_10              = models.BooleanField(default=False, verbose_name='Giá trị gia tăng 10%')
    vat_debit_account   = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='vat_debit_invoices',  verbose_name='TK Nợ (VAT 10%)')
    vat_credit_account  = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='vat_credit_invoices', verbose_name='TK Có (VAT 10%)')

    class Meta:
        verbose_name        = 'Hóa đơn mua hàng'
        verbose_name_plural = 'Hóa đơn mua hàng'

    @property
    def vat_amount(self):
        if self.vat_10:
            return self.total_amount * 10 / 100
        return 0

    def __str__(self):
        return self.invoice_number


class InvoiceLineItem(models.Model):
    invoice       = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='line_items', verbose_name='Hóa đơn')
    item_name     = models.CharField(max_length=200, verbose_name='Tên hàng hóa / dịch vụ')
    unit          = models.CharField(max_length=20, blank=True, verbose_name='Đơn vị tính')
    quantity      = models.DecimalField(max_digits=12, decimal_places=3, verbose_name='Số lượng')
    unit_price    = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Đơn giá chưa VAT')
    tax_rate      = models.DecimalField(max_digits=5, decimal_places=2, default=10, verbose_name='Thuế suất (%)')
    amount        = models.DecimalField(max_digits=18, decimal_places=2, editable=False, default=0, verbose_name='Thành tiền')

    class Meta:
        verbose_name        = 'Chi tiết hóa đơn'
        verbose_name_plural = 'Chi tiết dòng hàng hóa đơn'

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.invoice_id} — {self.item_name}'


class Voucher(models.Model):
    TYPE_CHOICES = [
        ('PT', 'Phiếu thu'),
        ('PC', 'Phiếu chi'),
    ]
    voucher_number  = models.CharField(max_length=10, primary_key=True, verbose_name='Số chứng từ')
    voucher_type    = models.CharField(max_length=3, choices=TYPE_CHOICES, verbose_name='Loại phiếu')
    voucher_date    = models.DateField(verbose_name='Ngày lập chứng từ')
    partner         = models.ForeignKey(Partner, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Đối tác')
    project         = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Dự án')
    debit_account   = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='debit_vouchers', verbose_name='Tài khoản ghi Nợ')
    credit_account  = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='credit_vouchers', verbose_name='Tài khoản ghi Có')
    amount          = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Số tiền (VNĐ)')
    bank_account    = models.ForeignKey(CompanyBankAccount, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Tài khoản ngân hàng')
    reason          = models.CharField(max_length=300, verbose_name='Lý do')
    created_by      = models.CharField(max_length=100, blank=True, verbose_name='Người lập')

    class Meta:
        verbose_name        = 'Phiếu thu/chi'
        verbose_name_plural = 'Phiếu thu/chi'

    def __str__(self):
        return f'{self.voucher_number} ({self.get_voucher_type_display()})'


class PhieuThu(Voucher):
    class Meta:
        proxy               = True
        verbose_name        = 'Phiếu thu'
        verbose_name_plural = 'Phiếu thu'


class PhieuChi(Voucher):
    class Meta:
        proxy               = True
        verbose_name        = 'Phiếu chi'
        verbose_name_plural = 'Phiếu chi'



class BankNotice(models.Model):
    TYPE_CHOICES = [
        ('GBN', 'Giấy báo nợ'),
        ('GBC', 'Giấy báo có'),
    ]

    notice_number    = models.CharField(max_length=10, primary_key=True, verbose_name='Số chứng từ giấy báo')
    notice_type      = models.CharField(max_length=5, choices=TYPE_CHOICES, verbose_name='Loại giấy báo')
    notice_date      = models.DateField(verbose_name='Ngày phát sinh giao dịch NH')
    partner          = models.ForeignKey(Partner, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Đối tác')
    project          = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Dự án')
    debit_account    = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='debit_notices', verbose_name='Tài khoản ghi Nợ')
    credit_account   = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='credit_notices', verbose_name='Tài khoản ghi Có')
    amount           = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Số tiền giao dịch')
    exchange_rate    = models.DecimalField(max_digits=12, decimal_places=4, default=1, verbose_name='Tỷ giá quy đổi')
    from_bank_account = models.ForeignKey(CompanyBankAccount, null=True, blank=True, on_delete=models.SET_NULL, related_name='outgoing_notices', verbose_name='Số TKNH chuyển đi')
    to_bank_account  = models.CharField(max_length=20, blank=True, verbose_name='Số TKNH chuyển đến')
    description      = models.CharField(max_length=300, blank=True, verbose_name='Nội dung giao dịch')
    linked_voucher   = models.ForeignKey(Voucher, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Liên kết phiếu thu/chi')

    class Meta:
        verbose_name        = 'Giấy báo nợ/có'
        verbose_name_plural = 'Giấy báo nợ/có ngân hàng'

    def __str__(self):
        return f'{self.notice_number} ({self.get_notice_type_display()})'


class GiayBaoNo(BankNotice):
    class Meta:
        proxy               = True
        verbose_name        = 'Giấy báo nợ'
        verbose_name_plural = 'Giấy báo nợ'


class GiayBaoCo(BankNotice):
    class Meta:
        proxy               = True
        verbose_name        = 'Giấy báo có'
        verbose_name_plural = 'Giấy báo có'
