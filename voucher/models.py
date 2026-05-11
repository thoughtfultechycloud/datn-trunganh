from django.contrib.auth.models import User
from django.db import models

from main.models import AccountCategory, CompanyBankAccount, Partner, Project


class Contract(models.Model):
    TYPE_CHOICES = [
        ('HDB', 'Hợp đồng bán ra'),
        ('HDM', 'Hợp đồng mua vào'),
    ]
    STATUS_CHOICES = [
        ('Hieu_luc', 'Hiệu lực'),
        ('Thanh_ly', 'Thanh lý'),
        ('Huy',      'Hủy'),
    ]

    contract_number = models.CharField(max_length=15, primary_key=True, verbose_name='Số hợp đồng')
    partner         = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Đối tác')
    project         = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name='Dự án')
    contract_type   = models.CharField(max_length=5, choices=TYPE_CHOICES, verbose_name='Loại hợp đồng')
    sign_date       = models.DateField(verbose_name='Ngày ký')
    effective_date  = models.DateField(verbose_name='Ngày hiệu lực')
    expiry_date     = models.DateField(null=True, blank=True, verbose_name='Ngày hết hạn')
    contract_value  = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Giá trị hợp đồng (VNĐ)')
    payment_terms   = models.CharField(max_length=500, blank=True, verbose_name='Điều khoản thanh toán')
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Hieu_luc', verbose_name='Trạng thái')
    attachment      = models.CharField(max_length=300, blank=True, verbose_name='File đính kèm')

    class Meta:
        verbose_name        = 'Hợp đồng'
        verbose_name_plural = 'Hợp đồng'
        ordering            = ['-sign_date', 'contract_number']

    def __str__(self):
        return self.contract_number


class PaymentSchedule(models.Model):
    STATUS_CHOICES = [
        ('Chua_den_han', 'Chưa đến hạn'),
        ('Den_han',      'Đến hạn'),
        ('Da_TT',        'Đã thanh toán'),
        ('Qua_han',      'Quá hạn'),
    ]

    contract       = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='payment_schedules', verbose_name='Hợp đồng')
    order          = models.PositiveSmallIntegerField(verbose_name='Thứ tự')
    description    = models.CharField(max_length=200, verbose_name='Mô tả đợt')
    completion_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='% hoàn thành')
    amount         = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Số tiền đợt (VNĐ)')
    due_date       = models.DateField(null=True, blank=True, verbose_name='Hạn ngày')
    actual_date    = models.DateField(null=True, blank=True, verbose_name='Ngày thực tế')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Chua_den_han', verbose_name='Trạng thái')

    class Meta:
        verbose_name        = 'Đợt thanh toán'
        verbose_name_plural = 'Đợt thanh toán'
        ordering            = ['contract', 'order']
        unique_together     = [('contract', 'order')]

    def __str__(self):
        return f'{self.contract_id} — Đợt {self.order}'


class AcceptanceRecord(models.Model):
    STATUS_CHOICES = [
        ('Nhap',   'Nháp'),
        ('Da_ky',  'Đã ký'),
        ('Da_huy', 'Đã hủy'),
    ]

    record_number = models.CharField(max_length=15, primary_key=True, verbose_name='Số biên bản nghiệm thu')
    contract         = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Hợp đồng liên quan')
    acceptance_date  = models.DateField(verbose_name='Ngày nghiệm thu')
    acceptance_value = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Giá trị nghiệm thu (VNĐ)')
    completion_pct   = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='% khối lượng hoàn thành')
    signer_a         = models.CharField(max_length=100, verbose_name='Người ký bên A')
    signer_b         = models.CharField(max_length=100, verbose_name='Người ký bên B')
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Nhap', verbose_name='Trạng thái')
    note             = models.CharField(max_length=300, blank=True, verbose_name='Ghi chú')

    class Meta:
        verbose_name        = 'Biên bản nghiệm thu'
        verbose_name_plural = 'Biên bản nghiệm thu'
        ordering            = ['-acceptance_date', 'record_number']

    def __str__(self):
        return self.record_number


class Invoice(models.Model):
    TYPE_CHOICES = [
        ('HDB', 'Hóa đơn bán ra'),
        ('HDM', 'Hóa đơn mua vào'),
    ]
    STATUS_CHOICES = [
        ('Chua_TT',  'Chưa thanh toán'),
        ('TT_1phan', 'Thanh toán 1 phần'),
        ('Da_TT',    'Đã thanh toán'),
    ]

    invoice_number = models.CharField(max_length=20, primary_key=True, verbose_name='Số hóa đơn GTGT')
    invoice_type   = models.CharField(max_length=5, choices=TYPE_CHOICES, verbose_name='Loại hóa đơn')
    invoice_date   = models.DateField(verbose_name='Ngày lập hóa đơn')
    partner        = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Đối tác')
    project        = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Dự án')
    acceptance     = models.ForeignKey(AcceptanceRecord, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Biên bản nghiệm thu')
    pre_tax_amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Tiền chưa thuế')
    tax_rate       = models.DecimalField(max_digits=5, decimal_places=2, default=10, verbose_name='Thuế suất VAT (%)')
    tax_amount     = models.DecimalField(max_digits=18, decimal_places=2, editable=False, default=0, verbose_name='Tiền thuế VAT')
    total_amount   = models.DecimalField(max_digits=18, decimal_places=2, editable=False, default=0, verbose_name='Tổng tiền')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Chua_TT', verbose_name='Trạng thái')

    class Meta:
        verbose_name        = 'Hóa đơn GTGT'
        verbose_name_plural = 'Hóa đơn GTGT'
        ordering            = ['-invoice_date', 'invoice_number']

    def save(self, *args, **kwargs):
        self.tax_amount   = self.pre_tax_amount * self.tax_rate / 100
        self.total_amount = self.pre_tax_amount + self.tax_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.invoice_number} ({self.get_invoice_type_display()})'


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
    STATUS_CHOICES = [
        ('Cho_duyet', 'Chờ duyệt'),
        ('Da_duyet',  'Đã duyệt'),
        ('Da_huy',    'Đã hủy'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Tien_mat',    'Tiền mặt'),
        ('Chuyen_khoan', 'Chuyển khoản'),
    ]

    voucher_number  = models.CharField(max_length=10, primary_key=True, verbose_name='Số chứng từ')
    voucher_type    = models.CharField(max_length=3, choices=TYPE_CHOICES, verbose_name='Loại phiếu')
    voucher_date    = models.DateField(verbose_name='Ngày lập chứng từ')
    partner         = models.ForeignKey(Partner, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Đối tác')
    project         = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Dự án')
    contract        = models.ForeignKey(Contract, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Hợp đồng')
    debit_account   = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='debit_vouchers', verbose_name='Tài khoản ghi Nợ')
    credit_account  = models.ForeignKey(AccountCategory, null=True, blank=True, on_delete=models.PROTECT, related_name='credit_vouchers', verbose_name='Tài khoản ghi Có')
    amount          = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Số tiền (VNĐ)')
    payment_method  = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, verbose_name='Hình thức')
    bank_account    = models.ForeignKey(CompanyBankAccount, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Tài khoản ngân hàng')
    reason          = models.CharField(max_length=300, verbose_name='Lý do')
    created_by      = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_vouchers', verbose_name='Người lập')
    approved_by     = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_vouchers', verbose_name='Người duyệt')
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Cho_duyet', verbose_name='Trạng thái')
    approved_at     = models.DateTimeField(null=True, blank=True, verbose_name='Ngày duyệt')

    class Meta:
        verbose_name        = 'Phiếu thu/chi'
        verbose_name_plural = 'Phiếu thu/chi'
        ordering            = ['-voucher_date', 'voucher_number']

    def __str__(self):
        return f'{self.voucher_number} ({self.get_voucher_type_display()})'


class VoucherLineItem(models.Model):
    voucher       = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='line_items', verbose_name='Phiếu thu/chi')
    amount        = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Số tiền')
    description   = models.CharField(max_length=200, blank=True, verbose_name='Diễn giải')

    class Meta:
        verbose_name        = 'Chi tiết phiếu thu/chi'
        verbose_name_plural = 'Chi tiết phiếu thu/chi'

    def __str__(self):
        return f'{self.voucher_id} — {self.description}'


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
        ordering            = ['-notice_date', 'notice_number']

    def __str__(self):
        return f'{self.notice_number} ({self.get_notice_type_display()})'
