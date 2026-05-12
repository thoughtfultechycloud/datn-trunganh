from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def tt_cong_ty(request):
    return render(request, 'info/tt_cong_ty.html', admin.site.each_context(request))


@staff_member_required
def hdsd(request):
    return render(request, 'info/hdsd.html', admin.site.each_context(request))
