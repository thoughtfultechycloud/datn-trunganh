from django.db import models


class SoCaiTK(models.Model):
    class Meta:
        managed             = False
        verbose_name        = 'Sổ cái TK'
        verbose_name_plural = 'Sổ cái TK'
        app_label           = 'ledger'


class SoChiTietTK(models.Model):
    class Meta:
        managed             = False
        verbose_name        = 'Sổ chi tiết TK'
        verbose_name_plural = 'Sổ chi tiết TK'
        app_label           = 'ledger'
