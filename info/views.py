from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def tt_cong_ty(request):
    return render(request, 'info/tt_cong_ty.html')


@staff_member_required
def hdsd(request):
    return render(request, 'info/hdsd.html')
