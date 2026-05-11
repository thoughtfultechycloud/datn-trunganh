from main.models import AccountOpeningBalance


class SoDuDauKi(AccountOpeningBalance):
    class Meta:
        proxy               = True
        verbose_name        = 'Số dư đầu kì'
        verbose_name_plural = 'Số dư đầu kì'
