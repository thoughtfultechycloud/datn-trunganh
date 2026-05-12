import io

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import BankNotice, Invoice, Voucher

PHIEU_CHI_TEMPLATE      = 'templates/file_templates/mau_phieu_chi_v3.docx'
PHIEU_THU_TEMPLATE      = 'templates/file_templates/mau_phieu_thu.docx'
PHIEU_MUA_HANG_TEMPLATE = 'templates/file_templates/template_phieu_mua_hang.docx'
GIAY_BAO_NO_TEMPLATE    = 'templates/file_templates/template_giay_bao_no.docx'
GIAY_BAO_CO_TEMPLATE    = 'templates/file_templates/template_giay_bao_co.docx'


@staff_member_required
def in_phieu_chi(request, pk):
    from docxtpl import DocxTemplate

    phieu = get_object_or_404(Voucher, voucher_number=pk, voucher_type='PC')

    tpl = DocxTemplate(PHIEU_CHI_TEMPLATE)
    tpl.render({
        'ngay':    phieu.voucher_date.day,
        'thang':   phieu.voucher_date.month,
        'nam':     phieu.voucher_date.year,
        'so':      phieu.voucher_number,
        'li_do': phieu.reason,
        'no':      phieu.debit_account.account_code  if phieu.debit_account  else '',
        'co':      phieu.credit_account.account_code if phieu.credit_account else '',
        'ho_ten':  phieu.partner.partner_name        if phieu.partner        else phieu.created_by,
        'so_tien': f"{phieu.amount:,.0f}",
    })

    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    response = HttpResponse(
        buf,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )
    response['Content-Disposition'] = f'attachment; filename="phieu_chi_{phieu.voucher_number}.docx"'
    return response


@staff_member_required
def in_phieu_thu(request, pk):
    from docxtpl import DocxTemplate

    phieu = get_object_or_404(Voucher, voucher_number=pk, voucher_type='PT')

    tpl = DocxTemplate(PHIEU_THU_TEMPLATE)
    tpl.render({
        'ngay':    phieu.voucher_date.day,
        'thang':   phieu.voucher_date.month,
        'nam':     phieu.voucher_date.year,
        'so':      phieu.voucher_number,
        'ly_do':   phieu.reason,
        'no':      phieu.debit_account.account_code  if phieu.debit_account  else '',
        'co':      phieu.credit_account.account_code if phieu.credit_account else '',
        'ho_ten':  phieu.partner.partner_name        if phieu.partner        else phieu.created_by,
        'dia_chi': phieu.partner.address             if phieu.partner        else '',
        'so_tien': f"{phieu.amount:,.0f}",
    })

    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    response = HttpResponse(
        buf,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )
    response['Content-Disposition'] = f'attachment; filename="phieu_thu_{phieu.voucher_number}.docx"'
    return response


@staff_member_required
def in_phieu_mua_hang(request, pk):
    from docxtpl import DocxTemplate

    inv = get_object_or_404(Invoice, invoice_number=pk)
    line_items = [
        {'ten': item.item_name, 'thanh_tien': f"{item.amount:,.0f}".replace(',', '.')}
        for item in inv.line_items.all()
    ]

    tpl = DocxTemplate(PHIEU_MUA_HANG_TEMPLATE)
    tpl.render({
        'so':              inv.invoice_number,
        'ngay':            inv.invoice_date.day,
        'thang':           inv.invoice_date.month,
        'nam':             inv.invoice_date.year,
        'don_vi_ban':      inv.seller_unit,
        'dia_chi_ban':     inv.seller_address,
        'li_do':           inv.reason,
        'nha_cung_cap':    inv.partner.partner_name if inv.partner else '',
        'ma_so_thue':      inv.tax_code,
        'dia_chi':         inv.address,
        'nguoi_giao_dich': inv.contact_person,
        'du_an':           str(inv.project) if inv.project else '',
        'no':              inv.debit_account.account_code  if inv.debit_account  else '',
        'co':              inv.credit_account.account_code if inv.credit_account else '',
        'tong_tien':       f"{inv.total_amount:,.0f}".replace(',', '.'),
        'vat_10':          inv.vat_10,
        'tien_thue':       f"{inv.vat_amount:,.0f}".replace(',', '.'),
        'no_vat':          inv.vat_debit_account.account_code  if inv.vat_debit_account  else '',
        'co_vat':          inv.vat_credit_account.account_code if inv.vat_credit_account else '',
        'mat_hang':        line_items,
        'tong_thanh_toan': f"{inv.total_amount + inv.vat_amount:,.0f}".replace(',', '.'),
        'mat_hang':        line_items,
    })
    
    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    response = HttpResponse(
        buf,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )
    response['Content-Disposition'] = f'attachment; filename="phieu_mua_hang_{inv.invoice_number}.docx"'
    return response


def _in_giay_bao(request, pk, notice_type, template_path, filename_prefix):
    from docxtpl import DocxTemplate
    n = get_object_or_404(BankNotice, notice_number=pk, notice_type=notice_type)
    tpl = DocxTemplate(template_path)
    tpl.render({
        'so':               n.notice_number,
        'ngay':             n.notice_date.day,
        'thang':            n.notice_date.month,
        'nam':              n.notice_date.year,
        'doi_tuong':        n.partner.partner_name if n.partner else '',
        'dia_chi':          n.partner.address if n.partner else '',
        'du_an':            str(n.project) if n.project else '',
        'so_tien':          f"{n.amount:,.0f}".replace(',', '.'),
        'ty_gia':           f"{n.exchange_rate:,.4f}",
        'tk_no':            n.debit_account.account_code  if n.debit_account  else '',
        'tk_co':            n.credit_account.account_code if n.credit_account else '',
        'tk_chuyen_di':     str(n.from_bank_account) if n.from_bank_account else '',
        'tk_chuyen_den':    n.to_bank_account,
        'noi_dung':         n.description,
    })
    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)
    response = HttpResponse(buf, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="{filename_prefix}_{n.notice_number}.docx"'
    return response


@staff_member_required
def in_giay_bao_no(request, pk):
    return _in_giay_bao(request, pk, 'GBN', GIAY_BAO_NO_TEMPLATE, 'giay_bao_no')


@staff_member_required
def in_giay_bao_co(request, pk):
    return _in_giay_bao(request, pk, 'GBC', GIAY_BAO_CO_TEMPLATE, 'giay_bao_co')
