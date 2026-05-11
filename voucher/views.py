import io

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Voucher

TEMPLATE_PATH = 'templates/file_templates/mau_phieu_chi_v2.docx'


@staff_member_required
def in_phieu_chi(request, pk):
    from docxtpl import DocxTemplate

    phieu = get_object_or_404(Voucher, voucher_number=pk, voucher_type='PC')

    tpl = DocxTemplate(TEMPLATE_PATH)
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
