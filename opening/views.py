from datetime import date

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from main.models import AccountOpeningBalance


@staff_member_required
@require_POST
def update_opening_balance(request, pk):
    try:
        AccountOpeningBalance.objects.filter(pk=pk).update(
            debit_balance=request.POST['debit_balance'],
            credit_balance=request.POST['credit_balance'],
            entry_date=date.today(),
            entered_by=request.user,
        )
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)
