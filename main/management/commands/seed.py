from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from main.models import Partner, Project, Bank, AccountCategory, CompanyBankAccount
from voucher.models import Invoice, InvoiceLineItem, Voucher, BankNotice


GROUPS = ['Nhân viên', 'Giám đốc', 'Trưởng dự án', 'Kế toán']


# (code, name, parent_code)
ACCOUNTS = [
    # Loại 1 - Tài sản ngắn hạn
    ('111',  'Tiền mặt',                                        None),
    ('1111', 'Tiền mặt VND',                                    '111'),
    ('112',  'Tiền gửi ngân hàng',                              None),
    ('1121', 'Tiền gửi ngân hàng VND',                          '112'),
    ('131',  'Phải thu khách hàng',                             None),
    ('133',  'Thuế GTGT được khấu trừ',                         None),
    ('1331', 'Thuế GTGT được khấu trừ của hàng hóa, dịch vụ',  '133'),
    ('141',  'Tạm ứng',                                         None),
    ('152',  'Nguyên liệu, vật liệu',                           None),
    ('153',  'Công cụ, dụng cụ',                                None),
    ('154',  'Chi phí SXKD dở dang',                            None),
    # Loại 2 - Tài sản dài hạn
    ('211',  'Tài sản cố định hữu hình',                        None),
    ('241',  'Xây dựng cơ bản dở dang',                         None),
    # Loại 3 - Nợ phải trả
    ('331',  'Phải trả người bán',                              None),
    ('333',  'Thuế và các khoản phải nộp Nhà nước',             None),
    ('3331', 'Thuế GTGT phải nộp',                              '333'),
    ('3334', 'Thuế thu nhập doanh nghiệp',                      '333'),
    ('334',  'Phải trả người lao động',                         None),
    ('338',  'Phải trả, phải nộp khác',                         None),
    ('341',  'Vay và nợ thuê tài chính',                        None),
    # Loại 4 - Vốn chủ sở hữu
    ('411',  'Vốn đầu tư của chủ sở hữu',                      None),
    ('421',  'Lợi nhuận sau thuế chưa phân phối',               None),
    # Loại 5 - Doanh thu
    ('511',  'Doanh thu bán hàng và cung cấp dịch vụ',          None),
    ('515',  'Doanh thu hoạt động tài chính',                   None),
    # Loại 6 - Chi phí
    ('621',  'Chi phí nguyên vật liệu trực tiếp',               None),
    ('622',  'Chi phí nhân công trực tiếp',                     None),
    ('623',  'Chi phí sử dụng máy thi công',                    None),
    ('627',  'Chi phí sản xuất chung',                          None),
    ('632',  'Giá vốn hàng bán',                                None),
    ('635',  'Chi phí tài chính',                               None),
    ('641',  'Chi phí bán hàng',                                None),
    ('642',  'Chi phí quản lý doanh nghiệp',                    None),
    # Loại 7, 8, 9
    ('711',  'Thu nhập khác',                                   None),
    ('811',  'Chi phí khác',                                    None),
    ('911',  'Xác định kết quả kinh doanh',                     None),
]

BANKS = [
    ('MB',   'Ngân hàng TMCP Quân đội',                  'Chi nhánh Hà Nội',     'Hà Nội'),
    ('VCB',  'Ngân hàng TMCP Ngoại thương Việt Nam',     'Chi nhánh Hoàn Kiếm',  'Hà Nội'),
    ('BIDV', 'Ngân hàng TMCP Đầu tư và Phát triển VN',  'Chi nhánh Hà Thành',   'Hà Nội'),
    ('TCB',  'Ngân hàng TMCP Kỹ Thương Việt Nam',        'Chi nhánh Cầu Giấy',   'Hà Nội'),
]

PARTNERS = [
    ('KH001', 'Tổng Công ty Đầu tư Phát triển Đô thị và Khu công nghiệp',  'KH', 'Hà Nội',      '0100100001', 'contact@udic.vn'),
    ('KH002', 'Công ty CP Đầu tư Xây dựng Hoà Bình',                        'KH', 'TP. HCM',     '0300100002', 'info@hoabinhgroup.vn'),
    ('KH003', 'Tổng Công ty Vinaconex',                                      'KH', 'Hà Nội',      '0100100003', 'info@vinaconex.vn'),
    ('KH004', 'Ban Quản lý Dự án Đầu tư Xây dựng Đà Nẵng',                  'KH', 'Đà Nẵng',     '0400100005', 'bql@danang.gov.vn'),
]

PROJECTS = [
    ('DA001', 'Chung cư cao tầng Hoàng Mai',               'KH001', date(2023, 3,  1),  date(2025, 6,  30), Decimal('85000000000'),  'Quận Hoàng Mai, Hà Nội'),
    ('DA002', 'Khu đô thị mới Tây Hồ Tây',                'KH001', date(2022, 6,  15), date(2025, 12, 31), Decimal('320000000000'), 'Tây Hồ, Hà Nội'),
    ('DA003', 'Tổ hợp chung cư – thương mại Bình Dương',  'KH002', date(2023, 1,  10), date(2026, 6,  30), Decimal('145000000000'), 'Thuận An, Bình Dương'),
    ('DA004', 'Nhà máy xử lý nước thải Tân Bình',         'KH002', date(2022, 9,  1),  date(2025, 3,  31), Decimal('95000000000'),  'Quận Tân Bình, TP. HCM'),
    ('DA005', 'Trụ sở làm việc Vinaconex Tower',           'KH003', date(2024, 2,  1),  date(2026, 8,  31), Decimal('210000000000'), 'Cầu Giấy, Hà Nội'),
    ('DA006', 'Khu công nghiệp Bắc Tiền Phong',            'KH003', date(2023, 7,  1),  date(2026, 6,  30), Decimal('185000000000'), 'Quảng Ninh'),
    ('DA007', 'Cầu vượt nút giao Điện Biên Phủ',           'KH004', date(2023, 5,  1),  date(2025, 7,  31), Decimal('112000000000'), 'Quận Hải Châu, Đà Nẵng'),
    ('DA008', 'Cảng Liên Chiểu giai đoạn 1',               'KH004', date(2023, 10, 1),  date(2027, 3,  31), Decimal('360000000000'), 'Liên Chiểu, Đà Nẵng'),
]

# (account_number, account_holder, bank_code, currency, balance)
COMPANY_BANK_ACCOUNTS = [
    ('0123456789',   'Công ty Cổ phần Công nghệ AI Box', 'MB',   'VND', Decimal('500000000')),
    ('9876543210',   'Công ty Cổ phần Công nghệ AI Box', 'VCB',  'VND', Decimal('1200000000')),
    ('1122334455',   'Công ty Cổ phần Công nghệ AI Box', 'BIDV', 'VND', Decimal('750000000')),
]

# Invoices: (number, date, seller, partner_code, project_code, debit_tk, credit_tk, vat, line_items)
INVOICES = [
    ('HD001', date(2026, 5, 10), 'Công ty TNHH Vật tư Xây dựng Miền Bắc', 'KH001', 'DA001',
     '152', '331', True,
     [('Xi măng PCB40 (50 tấn)', Decimal('45000000')),
      ('Cát vàng xây dựng (200 m³)', Decimal('30000000'))]),
    ('HD002', date(2026, 5, 5),  'Công ty CP Thiết bị Điện Việt Nam',      'KH002', 'DA003',
     '153', '331', True,
     [('Máy bơm công trường (2 cái)', Decimal('80000000')),
      ('Dây cáp điện 3 pha (500m)',   Decimal('35000000'))]),
    ('HD003', date(2026, 5, 20), 'Công ty TNHH Dịch vụ Cơ khí Hà Thành',  'KH003', 'DA005',
     '623', '331', False,
     [('Thuê máy đào 320D (30 ca)',   Decimal('90000000')),
      ('Thuê cần cẩu tháp (15 ngày)', Decimal('60000000'))]),
]

# Vouchers: (number, type, date, partner_code, project_code, debit_tk, credit_tk, amount, reason)
VOUCHERS = [
    # Phiếu thu
    ('PT001', 'PT', date(2026, 5, 15), 'KH001', 'DA001', '1111', '131',  Decimal('120000000'), 'Thu tiền tạm ứng hợp đồng DA001'),
    ('PT002', 'PT', date(2026, 5, 20), 'KH002', 'DA003', '1111', '131',  Decimal('85000000'),  'Thu thanh toán đợt 1 DA003'),
    ('PT003', 'PT', date(2026, 5, 10), 'KH004', 'DA007', '1111', '131',  Decimal('200000000'), 'Thu tiền nghiệm thu giai đoạn 1 DA007'),
    # Phiếu chi
    ('PC001', 'PC', date(2026, 5, 18), 'KH001', 'DA001', '331',  '1111', Decimal('75000000'),  'Chi thanh toán tiền vật tư HD001'),
    ('PC002', 'PC', date(2026, 5, 10), 'KH003', 'DA005', '642',  '1111', Decimal('25000000'),  'Chi phí quản lý dự án tháng 2/2025'),
    ('PC003', 'PC', date(2026, 5, 25), 'KH002', 'DA003', '622',  '1111', Decimal('48000000'),  'Chi lương nhân công tháng 3/2025'),
]

# BankNotices: (number, type, date, partner_code, project_code, debit_tk, credit_tk, amount, bank_acc_number, to_account, description)
BANK_NOTICES = [
    # Giấy báo nợ
    ('GBN001', 'GBN', date(2026, 5, 20), 'KH001', 'DA001', '331',  '1121', Decimal('115000000'), '0123456789', '1234567890123', 'Chuyển khoản thanh toán vật tư HD001'),
    ('GBN002', 'GBN', date(2026, 5, 15), 'KH003', 'DA005', '642',  '1121', Decimal('18000000'),  '9876543210', '9876543212345', 'Chuyển khoản phí dịch vụ văn phòng T2/2025'),
    ('GBN003', 'GBN', date(2026, 5, 28), 'KH002', 'DA003', '623',  '1121', Decimal('90000000'),  '1122334455', '1122334400001', 'Thanh toán thuê máy thi công DA003'),
    # Giấy báo có
    ('GBC001', 'GBC', date(2026, 5, 16), 'KH001', 'DA001', '1121', '131',  Decimal('300000000'), '0123456789', '',              'Khách hàng chuyển khoản tạm ứng DA001'),
    ('GBC002', 'GBC', date(2026, 5, 22), 'KH002', 'DA003', '1121', '131',  Decimal('150000000'), '9876543210', '',              'Thu thanh toán hợp đồng đợt 1 DA003'),
    ('GBC003', 'GBC', date(2026, 5, 12), 'KH004', 'DA008', '1121', '131',  Decimal('500000000'), '1122334455', '',              'Thu tạm ứng hợp đồng gói thầu DA008'),
]


class Command(BaseCommand):
    help = 'Seed accounts, banks, partners, projects and vouchers'

    def handle(self, *args, **kwargs):
        self._seed_groups()
        self._seed_sample_user()
        self._seed_accounts()
        self._seed_banks()
        self._seed_partners()
        self._seed_projects()
        self._seed_company_bank_accounts()
        self._seed_invoices()
        self._seed_vouchers()
        self._seed_bank_notices()
        self.stdout.write(self.style.SUCCESS('Seeding hoàn tất.'))

    def _seed_groups(self):
        for name in GROUPS:
            Group.objects.get_or_create(name=name)
        self.stdout.write(f'  Nhóm quyền: {len(GROUPS)} bản ghi.')

    def _seed_sample_user(self):
        username = 'truongduan'
        user, created = User.objects.get_or_create(
            username=username,
            defaults=dict(
                first_name='Nguyễn Văn',
                last_name='An',
                email='truongduan@aibox.vn',
                is_staff=True,
            ),
        )
        if created:
            user.set_password('aibox@123')
            user.save()
        group = Group.objects.get(name='Trưởng dự án')
        user.groups.set([group])
        self.stdout.write(f'  User mẫu: {username} ({"tạo mới" if created else "đã tồn tại"}).')

    def _seed_accounts(self):
        for code, name, parent_code in ACCOUNTS:
            parent = AccountCategory.objects.filter(account_code=parent_code).first() if parent_code else None
            AccountCategory.objects.get_or_create(
                account_code=code,
                defaults=dict(account_name=name, parent=parent, is_active=True),
            )
        self.stdout.write(f'  Tài khoản kế toán: {len(ACCOUNTS)} bản ghi.')

    def _seed_banks(self):
        for code, name, branch, address in BANKS:
            Bank.objects.get_or_create(
                bank_code=code,
                defaults=dict(bank_name=name, branch=branch, address=address, is_active=True),
            )
        self.stdout.write(f'  Ngân hàng: {len(BANKS)} bản ghi.')

    def _seed_partners(self):
        for code, name, ptype, address, tax, email in PARTNERS:
            Partner.objects.get_or_create(
                partner_code=code,
                defaults=dict(partner_name=name, partner_type=ptype, address=address,
                              tax_code=tax, email=email, is_active=True),
            )
        self.stdout.write(f'  Đối tác: {len(PARTNERS)} bản ghi.')

    def _seed_projects(self):
        manager = User.objects.filter(is_superuser=True).first()
        count = 0
        for code, name, investor_code, start, end, value, location in PROJECTS:
            investor = Partner.objects.get(partner_code=investor_code)
            _, created = Project.objects.get_or_create(
                project_code=code,
                defaults=dict(project_name=name, investor=investor, start_date=start,
                              end_date=end, contract_value=value, location=location, manager=manager),
            )
            if created:
                count += 1
        self.stdout.write(f'  Dự án: {count} tạo mới, {len(PROJECTS) - count} đã tồn tại.')

    def _seed_company_bank_accounts(self):
        count = 0
        for acc_no, holder, bank_code, currency, balance in COMPANY_BANK_ACCOUNTS:
            bank = Bank.objects.get(bank_code=bank_code)
            _, created = CompanyBankAccount.objects.get_or_create(
                account_number=acc_no,
                defaults=dict(account_holder=holder, bank=bank, currency=currency,
                              balance=balance, is_active=True),
            )
            if created:
                count += 1
        self.stdout.write(f'  TK ngân hàng công ty: {count} tạo mới.')

    def _seed_invoices(self):
        count = 0
        for number, inv_date, seller, partner_code, project_code, debit_tk, credit_tk, vat, items in INVOICES:
            Invoice.objects.filter(invoice_number=number).delete()
            partner = Partner.objects.get(partner_code=partner_code)
            project = Project.objects.get(project_code=project_code)
            debit   = AccountCategory.objects.get(account_code=debit_tk)
            credit  = AccountCategory.objects.get(account_code=credit_tk)
            vat_debit  = AccountCategory.objects.get(account_code='1331') if vat else None
            vat_credit = AccountCategory.objects.get(account_code='331')  if vat else None

            inv = Invoice.objects.create(
                invoice_number=number, invoice_date=inv_date,
                seller_unit=seller, partner=partner, project=project,
                debit_account=debit, credit_account=credit,
                vat_10=vat, vat_debit_account=vat_debit, vat_credit_account=vat_credit,
            )
            total = Decimal('0')
            for item_name, amount in items:
                InvoiceLineItem.objects.create(invoice=inv, item_name=item_name, amount=amount)
                total += amount
            Invoice.objects.filter(pk=inv.pk).update(total_amount=total)
            count += 1
        self.stdout.write(f'  Phiếu mua hàng: {count} tạo mới.')

    def _seed_vouchers(self):
        count = 0
        for number, vtype, vdate, partner_code, project_code, debit_tk, credit_tk, amount, reason in VOUCHERS:
            Voucher.objects.filter(voucher_number=number).delete()
            partner = Partner.objects.get(partner_code=partner_code)
            project = Project.objects.get(project_code=project_code)
            debit   = AccountCategory.objects.get(account_code=debit_tk)
            credit  = AccountCategory.objects.get(account_code=credit_tk)
            Voucher.objects.create(
                voucher_number=number, voucher_type=vtype, voucher_date=vdate,
                partner=partner, project=project,
                debit_account=debit, credit_account=credit,
                amount=amount, reason=reason, created_by='Admin',
            )
            count += 1
        self.stdout.write(f'  Phiếu thu/chi: {count} tạo mới.')

    def _seed_bank_notices(self):
        count = 0
        for number, ntype, ndate, partner_code, project_code, debit_tk, credit_tk, amount, bank_acc_no, to_acc, desc in BANK_NOTICES:
            BankNotice.objects.filter(notice_number=number).delete()
            partner    = Partner.objects.get(partner_code=partner_code)
            project    = Project.objects.get(project_code=project_code)
            debit      = AccountCategory.objects.get(account_code=debit_tk)
            credit     = AccountCategory.objects.get(account_code=credit_tk)
            bank_acc   = CompanyBankAccount.objects.filter(account_number=bank_acc_no).first()
            BankNotice.objects.create(
                notice_number=number, notice_type=ntype, notice_date=ndate,
                partner=partner, project=project,
                debit_account=debit, credit_account=credit,
                amount=amount, from_bank_account=bank_acc, to_bank_account=to_acc,
                description=desc,
            )
            count += 1
        self.stdout.write(f'  Giấy báo nợ/có: {count} tạo mới.')
