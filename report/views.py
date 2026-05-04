from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def debt_report(request):
    return render(request, 'report/debt_report.html')
