from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def so_cai_tk(request):
    return render(request, 'ledger/so_cai_tk.html')


@staff_member_required
def so_chi_tiet_tk(request):
    return render(request, 'ledger/so_chi_tiet_tk.html')
