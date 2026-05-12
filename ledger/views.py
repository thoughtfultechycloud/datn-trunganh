from decimal import Decimal

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render

from main.models import AccountCategory, AccountOpeningBalance
from voucher.models import BankNotice, Invoice, Voucher


def get_so_cai_context(request):
    accounts = AccountCategory.objects.filter(is_active=True).order_by('account_code')
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

    # --- Số dư đầu kỳ ---
    try:
        ob = AccountOpeningBalance.objects.get(account_id=account_id)
        no_dau = ob.debit_balance
        co_dau = ob.credit_balance
    except AccountOpeningBalance.DoesNotExist:
        no_dau = co_dau = Decimal('0')

    # --- Phát sinh từ Phiếu thu/chi ---
    rows = []
    vouchers = (
        Voucher.objects
        .filter(
            Q(debit_account_id=account_id) | Q(credit_account_id=account_id),
            voucher_date__gte=tu_ngay,
            voucher_date__lte=den_ngay,
        )
        .select_related('partner', 'debit_account', 'credit_account')
        .order_by('voucher_date', 'voucher_number')
    )
    for v in vouchers:
        is_debit = v.debit_account_id == account_id
        tk_du    = v.credit_account.account_code if is_debit else (v.debit_account.account_code if v.debit_account else '')
        rows.append({
            'ngay':         v.voucher_date,
            'so_ct':        v.voucher_number,
            'dien_giai':    v.reason,
            'doi_tuong':    v.partner.partner_name if v.partner else '',
            'tk_doi_ung':   tk_du,
            'phat_sinh_no': v.amount if is_debit else Decimal('0'),
            'phat_sinh_co': Decimal('0') if is_debit else v.amount,
        })

    # --- Phát sinh từ Giấy báo nợ/có ---
    notices = (
        BankNotice.objects
        .filter(
            Q(debit_account_id=account_id) | Q(credit_account_id=account_id),
            notice_date__gte=tu_ngay,
            notice_date__lte=den_ngay,
        )
        .select_related('partner', 'debit_account', 'credit_account')
        .order_by('notice_date', 'notice_number')
    )
    for n in notices:
        is_debit = n.debit_account_id == account_id
        tk_du    = n.credit_account.account_code if is_debit else (n.debit_account.account_code if n.debit_account else '')
        rows.append({
            'ngay':         n.notice_date,
            'so_ct':        n.notice_number,
            'dien_giai':    n.description,
            'doi_tuong':    n.partner.partner_name if n.partner else '',
            'tk_doi_ung':   tk_du,
            'phat_sinh_no': n.amount if is_debit else Decimal('0'),
            'phat_sinh_co': Decimal('0') if is_debit else n.amount,
        })

    # --- Phát sinh từ Hóa đơn mua hàng ---
    invoices = (
        Invoice.objects
        .filter(
            Q(debit_account_id=account_id)     | Q(credit_account_id=account_id) |
            Q(vat_debit_account_id=account_id) | Q(vat_credit_account_id=account_id),
            invoice_date__gte=tu_ngay,
            invoice_date__lte=den_ngay,
        )
        .select_related('partner', 'debit_account', 'credit_account', 'vat_debit_account', 'vat_credit_account')
        .order_by('invoice_date', 'invoice_number')
    )
    for inv in invoices:
        dien_giai = inv.description or f'Hóa đơn {inv.invoice_number}'
        doi_tuong = inv.partner.partner_name if inv.partner else ''

        # Bút toán chính (total_amount)
        if inv.debit_account_id == account_id or inv.credit_account_id == account_id:
            is_debit = inv.debit_account_id == account_id
            tk_du    = inv.credit_account.account_code if is_debit else (inv.debit_account.account_code if inv.debit_account else '')
            rows.append({
                'ngay':         inv.invoice_date,
                'so_ct':        inv.invoice_number,
                'dien_giai':    dien_giai,
                'doi_tuong':    doi_tuong,
                'tk_doi_ung':   tk_du,
                'phat_sinh_no': inv.total_amount if is_debit else Decimal('0'),
                'phat_sinh_co': Decimal('0') if is_debit else inv.total_amount,
            })

        # Bút toán VAT (total_amount × 10%)
        if inv.vat_10 and (inv.vat_debit_account_id == account_id or inv.vat_credit_account_id == account_id):
            vat_amt  = inv.total_amount * Decimal('0.10')
            is_debit = inv.vat_debit_account_id == account_id
            tk_du    = inv.vat_credit_account.account_code if is_debit else (inv.vat_debit_account.account_code if inv.vat_debit_account else '')
            rows.append({
                'ngay':         inv.invoice_date,
                'so_ct':        inv.invoice_number,
                'dien_giai':    f'{dien_giai} (VAT 10%)',
                'doi_tuong':    doi_tuong,
                'tk_doi_ung':   tk_du,
                'phat_sinh_no': vat_amt if is_debit else Decimal('0'),
                'phat_sinh_co': Decimal('0') if is_debit else vat_amt,
            })

    rows.sort(key=lambda r: (r['ngay'], r['so_ct']))

    tong_no = sum(r['phat_sinh_no'] for r in rows)
    tong_co = sum(r['phat_sinh_co'] for r in rows)

    # Số dư cuối kỳ (net)
    net_dau  = no_dau - co_dau
    net_cuoi = net_dau + tong_no - tong_co
    no_cuoi  = max(net_cuoi, Decimal('0'))
    co_cuoi  = max(-net_cuoi, Decimal('0'))

    ctx.update({
        'show_result':    True,
        'selected_name':  f"{account_id}",
        'no_dau':         no_dau,
        'co_dau':         co_dau,
        'rows':           rows,
        'tong_no':        tong_no,
        'tong_co':        tong_co,
        'no_cuoi':        no_cuoi,
        'co_cuoi':        co_cuoi,
    })
    return ctx


def get_so_chi_tiet_context(request):
    ctx = get_so_cai_context(request)
    if not ctx.get('show_result'):
        return ctx

    # Tính cột Tồn (số dư lũy kế sau mỗi dòng)
    running = ctx['no_dau'] - ctx['co_dau']
    for row in ctx['rows']:
        running += row['phat_sinh_no'] - row['phat_sinh_co']
        row['ton']      = abs(running)
        row['ton_loai'] = 'Nợ' if running >= 0 else 'Có'

    return ctx


@staff_member_required
def so_cai_tk(request):
    ctx = {**admin.site.each_context(request), **get_so_cai_context(request)}
    return render(request, 'ledger/so_cai_tk.html', ctx)


@staff_member_required
def so_chi_tiet_tk(request):
    ctx = {**admin.site.each_context(request), **get_so_chi_tiet_context(request)}
    return render(request, 'ledger/so_chi_tiet_tk.html', ctx)
