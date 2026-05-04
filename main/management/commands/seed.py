from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from main.models import Partner, Project


PARTNERS = [
    ('KH001', 'Tổng Công ty Đầu tư Phát triển Đô thị',      'KH', 'Hà Nội',        '0100100001', 'contact@udic.vn'),
    ('KH002', 'Công ty CP Đầu tư Xây dựng Hoà Bình',         'KH', 'TP. HCM',       '0300100002', 'info@hoabinhgroup.vn'),
    ('KH003', 'Tổng Công ty Vinaconex',                      'KH', 'Hà Nội',        '0100100003', 'info@vinaconex.vn'),
    ('KH004', 'Công ty CP Đầu tư Hạ tầng Kỹ thuật TP.HCM',  'KH', 'TP. HCM',       '0300100004', 'citenco@hcm.vn'),
    ('KH005', 'Ban Quản lý Dự án Đầu tư Xây dựng Đà Nẵng',  'KH', 'Đà Nẵng',      '0400100005', 'bql@danang.gov.vn'),
]

PROJECTS = [
    ('DA001', 'Chung cư cao tầng Hoàng Mai',           'KH001', date(2023, 3, 1),  date(2025, 6, 30),  Decimal('85000000000'),  'Quận Hoàng Mai, Hà Nội',           'Dang_thi_cong'),
    ('DA002', 'Khu đô thị Vinhomes Ocean Park 2',      'KH002', date(2022, 6, 15), date(2025, 12, 31), Decimal('320000000000'), 'Hưng Yên',                          'Dang_thi_cong'),
    ('DA003', 'Cầu vượt nút giao Nguyễn Văn Linh',    'KH005', date(2023, 1, 10), date(2024, 12, 31), Decimal('95000000000'),  'Quận 7, TP. HCM',                  'Hoan_thanh'),
    ('DA004', 'Nhà máy xử lý nước thải Bình Dương',   'KH003', date(2022, 9, 1),  date(2025, 3, 31),  Decimal('125000000000'), 'Thuận An, Bình Dương',              'Dang_thi_cong'),
    ('DA005', 'Trường THCS Nguyễn Trãi mở rộng',      'KH005', date(2024, 2, 1),  date(2024, 11, 30), Decimal('18500000000'),  'Quận Hải Châu, Đà Nẵng',           'Hoan_thanh'),
    ('DA006', 'Khu công nghiệp Bắc Tiền Phong',       'KH001', date(2023, 7, 1),  date(2026, 6, 30),  Decimal('210000000000'), 'Quảng Ninh',                        'Dang_thi_cong'),
    ('DA007', 'Bệnh viện Đa khoa Trung ương Huế MR',  'KH003', date(2022, 4, 1),  date(2025, 9, 30),  Decimal('145000000000'), 'TP. Huế, Thừa Thiên Huế',          'Dang_thi_cong'),
    ('DA008', 'Tuyến đường sắt đô thị số 3 gói 3',    'KH004', date(2021, 11, 1), date(2026, 12, 31), Decimal('580000000000'), 'Hà Nội',                            'Dang_thi_cong'),
    ('DA009', 'Cảng Liên Chiểu giai đoạn 1',          'KH005', date(2023, 10, 1), date(2027, 3, 31),  Decimal('360000000000'), 'Liên Chiểu, Đà Nẵng',              'Dang_thi_cong'),
    ('DA010', 'Khu dân cư Đại Kim – Định Công',       'KH002', date(2022, 1, 15), date(2024, 10, 31), Decimal('72000000000'),  'Quận Hoàng Mai, Hà Nội',           'Hoan_thanh'),
    ('DA011', 'Tổ hợp thương mại Sun Grand City',     'KH001', date(2023, 5, 1),  date(2026, 4, 30),  Decimal('195000000000'), 'Quận 1, TP. HCM',                  'Dang_thi_cong'),
    ('DA012', 'Nhà máy điện gió Bạc Liêu MR',         'KH003', date(2024, 1, 1),  date(2026, 1, 31),  Decimal('285000000000'), 'Bạc Liêu',                         'Dang_thi_cong'),
    ('DA013', 'Hầm chui Điện Biên Phủ – Lê Văn Sỹ',  'KH004', date(2023, 8, 1),  date(2025, 7, 31),  Decimal('112000000000'), 'Quận 3, TP. HCM',                  'Tam_dung'),
    ('DA014', 'Khu tái định cư Thủ Thiêm',            'KH004', date(2022, 3, 1),  date(2025, 6, 30),  Decimal('168000000000'), 'TP. Thủ Đức, TP. HCM',             'Dang_thi_cong'),
    ('DA015', 'Trạm biến áp 500kV Vân Phong',         'KH003', date(2023, 6, 1),  date(2025, 12, 31), Decimal('98000000000'),  'Khánh Hòa',                        'Dang_thi_cong'),
]


class Command(BaseCommand):
    help = 'Seed database with 15 sample projects'

    def handle(self, *args, **kwargs):
        self._seed_partners()
        self._seed_projects()
        self.stdout.write(self.style.SUCCESS('Seeding completed successfully.'))

    def _seed_partners(self):
        for code, name, ptype, address, tax, email in PARTNERS:
            Partner.objects.get_or_create(
                partner_code=code,
                defaults=dict(
                    partner_name=name,
                    partner_type=ptype,
                    address=address,
                    tax_code=tax,
                    email=email,
                    is_active=True,
                ),
            )
        self.stdout.write(f'  Partners: {len(PARTNERS)} upserted.')

    def _seed_projects(self):
        manager = User.objects.filter(groups__id=1).first()
        count = 0
        for code, name, investor_code, start, end, value, location, status in PROJECTS:
            investor = Partner.objects.get(partner_code=investor_code)
            _, created = Project.objects.get_or_create(
                project_code=code,
                defaults=dict(
                    project_name=name,
                    investor=investor,
                    start_date=start,
                    end_date=end,
                    contract_value=value,
                    location=location,
                    manager=manager,
                    status=status,
                ),
            )
            if created:
                count += 1
        self.stdout.write(f'  Projects: {count} created, {len(PROJECTS) - count} already existed.')
