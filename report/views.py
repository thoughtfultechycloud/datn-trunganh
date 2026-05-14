from decimal import Decimal

import io

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from main.models import AccountCategory, PartnerOpeningBalance, Project
from voucher.models import BankNotice, Invoice, Voucher


def get_bao_cao_no_context(request):
    accounts   = AccountCategory.objects.filter(is_active=True).order_by('account_code')
    account_id = request.GET.get('account', '')
    tu_ngay    = request.GET.get('tu_ngay', '')
    den_ngay   = request.GET.get('den_ngay', '')

    ctx = {
        'accounts':         accounts,
        'selected_account': account_id,
        'tu_ngay':          tu_ngay,
        'den_ngay':         den_ngay,
        'show_result':      False,
    }

    if not (account_id and tu_ngay and den_ngay):
        return ctx

    # --- Số dư đầu kỳ theo đối tác ---
    ob_qs = PartnerOpeningBalance.objects.filter(
        account_id=account_id
    ).select_related('partner', 'project')

    ob_map = {}  # partner_id -> {no, co}
    for ob in ob_qs:
        pid = ob.partner_id
        if pid not in ob_map:
            ob_map[pid] = {'partner': ob.partner, 'no_dau': Decimal('0'), 'co_dau': Decimal('0')}
        ob_map[pid]['no_dau'] += ob.debit_balance
        ob_map[pid]['co_dau'] += ob.credit_balance

    # --- Phát sinh trong kỳ từ Voucher ---
    ps_map = {}  # partner_id -> {no, co}

    def add_ps(partner, amount, is_debit):
        pid = partner.pk if partner else None
        if pid not in ps_map:
            ps_map[pid] = {
                'partner': partner,
                'ps_no':   Decimal('0'),
                'ps_co':   Decimal('0'),
            }
        if is_debit:
            ps_map[pid]['ps_no'] += amount
        else:
            ps_map[pid]['ps_co'] += amount

    vouchers = Voucher.objects.filter(
        Q(debit_account_id=account_id) | Q(credit_account_id=account_id),
        voucher_date__gte=tu_ngay,
        voucher_date__lte=den_ngay,
    ).select_related('partner')

    for v in vouchers:
        add_ps(v.partner, v.amount, v.debit_account_id == account_id)

    notices = BankNotice.objects.filter(
        Q(debit_account_id=account_id) | Q(credit_account_id=account_id),
        notice_date__gte=tu_ngay,
        notice_date__lte=den_ngay,
    ).select_related('partner')

    for n in notices:
        add_ps(n.partner, n.amount, n.debit_account_id == account_id)

    invoices = Invoice.objects.filter(
        Q(debit_account_id=account_id) | Q(credit_account_id=account_id) |
        Q(vat_debit_account_id=account_id) | Q(vat_credit_account_id=account_id),
        invoice_date__gte=tu_ngay,
        invoice_date__lte=den_ngay,
    ).select_related('partner')

    for inv in invoices:
        if inv.debit_account_id == account_id or inv.credit_account_id == account_id:
            add_ps(inv.partner, inv.total_amount, inv.debit_account_id == account_id)
        if inv.vat_10 and (inv.vat_debit_account_id == account_id or inv.vat_credit_account_id == account_id):
            vat_amt = inv.total_amount * Decimal('0.10')
            add_ps(inv.partner, vat_amt, inv.vat_debit_account_id == account_id)

    # --- Tổng hợp theo đối tác ---
    all_partners = set(ob_map) | set(ps_map)
    rows = []
    for pid in all_partners:
        ob  = ob_map.get(pid, {})
        ps  = ps_map.get(pid, {})
        partner = ob.get('partner') or ps.get('partner')

        no_dau = ob.get('no_dau', Decimal('0'))
        co_dau = ob.get('co_dau', Decimal('0'))
        ps_no  = ps.get('ps_no',  Decimal('0'))
        ps_co  = ps.get('ps_co',  Decimal('0'))

        net_cuoi = (no_dau - co_dau) + ps_no - ps_co
        no_cuoi  = max(net_cuoi,  Decimal('0'))
        co_cuoi  = max(-net_cuoi, Decimal('0'))

        rows.append({
            'partner':  partner.partner_name if partner else '(Không xác định)',
            'no_dau':   no_dau,
            'co_dau':   co_dau,
            'ps_no':    ps_no,
            'ps_co':    ps_co,
            'no_cuoi':  no_cuoi,
            'co_cuoi':  co_cuoi,
        })

    rows.sort(key=lambda r: r['partner'])

    tong = {k: sum(r[k] for r in rows) for k in ('no_dau', 'co_dau', 'ps_no', 'ps_co', 'no_cuoi', 'co_cuoi')}

    ctx.update({'show_result': True, 'rows': rows, 'tong': tong})
    return ctx


def _fmt(value):
    try:
        return f"{int(value):,}".replace(',', '.')
    except (TypeError, ValueError):
        return ''


def _fmt_date(d):
    try:
        from datetime import datetime
        return datetime.strptime(d, '%Y-%m-%d').strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return d


@staff_member_required
def bao_cao_no_pt(request):
    request.GET = request.GET.copy()
    request.GET['account'] = '131'
    ctx = {**admin.site.each_context(request), **get_bao_cao_no_context(request)}
    return render(request, 'report/bao_cao_no_pt.html', ctx)


@staff_member_required
def xuat_bao_cao_no_pt(request):
    from docxtpl import DocxTemplate

    request.GET = request.GET.copy()
    request.GET['account'] = '131'
    data = get_bao_cao_no_context(request)
    if not data.get('show_result'):
        from django.http import HttpResponseBadRequest
        return HttpResponseBadRequest('Thiếu tham số lọc.')

    rows = [
        {
            'doi_tuong': r['partner'],
            'no_dau':    _fmt(r['no_dau'])  if r['no_dau']  else '',
            'co_dau':    _fmt(r['co_dau'])  if r['co_dau']  else '',
            'ps_no':     _fmt(r['ps_no'])   if r['ps_no']   else '',
            'ps_co':     _fmt(r['ps_co'])   if r['ps_co']   else '',
            'no_cuoi':   _fmt(r['no_cuoi']) if r['no_cuoi'] else '',
            'co_cuoi':   _fmt(r['co_cuoi']) if r['co_cuoi'] else '',
        }
        for r in data['rows']
    ]
    tong = data['tong']

    tpl = DocxTemplate('templates/file_templates/template_bao_cao_cong_no.docx')
    tpl.render({
        'tai_khoan': data['selected_account'],
        'tu_ngay':   _fmt_date(data['tu_ngay']),
        'den_ngay':  _fmt_date(data['den_ngay']),
        'rows':      rows,
        'tong_no_dau':  _fmt(tong['no_dau']),
        'tong_co_dau':  _fmt(tong['co_dau']),
        'tong_ps_no':   _fmt(tong['ps_no']),
        'tong_ps_co':   _fmt(tong['ps_co']),
        'tong_no_cuoi': _fmt(tong['no_cuoi']),
        'tong_co_cuoi': _fmt(tong['co_cuoi']),
    })

    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    account_id = data['selected_account']
    response = HttpResponse(buf, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="bao_cao_no_pt_{account_id}.docx"'
    return response


@staff_member_required
def bao_cao_no_ptra(request):
    request.GET = request.GET.copy()
    request.GET['account'] = '331'
    ctx = {**admin.site.each_context(request), **get_bao_cao_no_context(request)}
    return render(request, 'report/bao_cao_no_ptra.html', ctx)


@staff_member_required
def xuat_bao_cao_no_ptra(request):
    from docxtpl import DocxTemplate

    request.GET = request.GET.copy()
    request.GET['account'] = '331'
    data = get_bao_cao_no_context(request)
    if not data.get('show_result'):
        from django.http import HttpResponseBadRequest
        return HttpResponseBadRequest('Thiếu tham số lọc.')

    rows = [
        {
            'doi_tuong': r['partner'],
            'no_dau':    _fmt(r['no_dau'])  if r['no_dau']  else '',
            'co_dau':    _fmt(r['co_dau'])  if r['co_dau']  else '',
            'ps_no':     _fmt(r['ps_no'])   if r['ps_no']   else '',
            'ps_co':     _fmt(r['ps_co'])   if r['ps_co']   else '',
            'no_cuoi':   _fmt(r['no_cuoi']) if r['no_cuoi'] else '',
            'co_cuoi':   _fmt(r['co_cuoi']) if r['co_cuoi'] else '',
        }
        for r in data['rows']
    ]
    tong = data['tong']

    tpl = DocxTemplate('templates/file_templates/template_bao_cao_cong_no.docx')
    tpl.render({
        'tai_khoan':    data['selected_account'],
        'tu_ngay':      _fmt_date(data['tu_ngay']),
        'den_ngay':     _fmt_date(data['den_ngay']),
        'rows':         rows,
        'tong_no_dau':  _fmt(tong['no_dau']),
        'tong_co_dau':  _fmt(tong['co_dau']),
        'tong_ps_no':   _fmt(tong['ps_no']),
        'tong_ps_co':   _fmt(tong['ps_co']),
        'tong_no_cuoi': _fmt(tong['no_cuoi']),
        'tong_co_cuoi': _fmt(tong['co_cuoi']),
    })

    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    response = HttpResponse(buf, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="bao_cao_no_ptra_331.docx"'
    return response


def get_bang_ke_chi_tien_context(request):
    projects   = Project.objects.all().order_by('project_code')
    project_id = request.GET.get('project', '')
    tu_ngay    = request.GET.get('tu_ngay', '')
    den_ngay   = request.GET.get('den_ngay', '')

    ctx = {
        'projects':         projects,
        'selected_project': project_id,
        'tu_ngay':          tu_ngay,
        'den_ngay':         den_ngay,
        'show_result':      False,
    }

    if not (project_id and tu_ngay and den_ngay):
        return ctx

    qs = Voucher.objects.filter(
        voucher_type='PC',
        project_id=project_id,
        voucher_date__gte=tu_ngay,
        voucher_date__lte=den_ngay,
    ).select_related('partner', 'project', 'debit_account', 'credit_account').order_by('voucher_date', 'voucher_number')

    rows = []
    for i, v in enumerate(qs, start=1):
        rows.append({
            'stt':            i,
            'voucher_number': v.voucher_number,
            'voucher_date':   v.voucher_date,
            'partner':        v.partner.partner_name if v.partner else '',
            'reason':         v.reason,
            'debit_account':  v.debit_account.account_code if v.debit_account else '',
            'credit_account': v.credit_account.account_code if v.credit_account else '',
            'amount':         v.amount,
        })

    tong_tien = sum(r['amount'] for r in rows)
    try:
        project_obj = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        project_obj = None

    ctx.update({
        'show_result':  True,
        'rows':         rows,
        'tong_tien':    tong_tien,
        'project_obj':  project_obj,
    })
    return ctx


@staff_member_required
def bang_ke_chi_tien(request):
    ctx = {**admin.site.each_context(request), **get_bang_ke_chi_tien_context(request)}
    return render(request, 'report/bang_ke_chi_tien.html', ctx)


@staff_member_required
def xuat_bang_ke_chi_tien(request):
    from docxtpl import DocxTemplate

    data = get_bang_ke_chi_tien_context(request)
    if not data.get('show_result'):
        from django.http import HttpResponseBadRequest
        return HttpResponseBadRequest('Thiếu tham số lọc.')

    rows = [
        {
            'stt':            r['stt'],
            'so_phieu':       r['voucher_number'],
            'ngay':           r['voucher_date'].strftime('%d/%m/%Y'),
            'doi_tac':        r['partner'],
            'ly_do':          r['reason'],
            'tk_no':          r['debit_account'],
            'tk_co':          r['credit_account'],
            'so_tien':        f"{r['amount']:,.0f}".replace(',', '.'),
        }
        for r in data['rows']
    ]

    tpl = DocxTemplate('templates/file_templates/template_bang_ke_chi_tien.docx')
    tpl.render({
        'du_an':     str(data['project_obj']) if data['project_obj'] else '',
        'tu_ngay':   _fmt_date(data['tu_ngay']),
        'den_ngay':  _fmt_date(data['den_ngay']),
        'rows':      rows,
        'tong_tien': f"{data['tong_tien']:,.0f}".replace(',', '.'),
    })

    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    response = HttpResponse(buf, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    project_id = request.GET.get('project', 'unknown')
    response['Content-Disposition'] = f'attachment; filename="bang_ke_chi_tien_{project_id}.docx"'
    return response
