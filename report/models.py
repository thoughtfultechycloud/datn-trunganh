from django.db import models


class DebtReport(models.Model):
    class Meta:
        managed      = False
        verbose_name = 'Báo cáo công nợ'
        verbose_name_plural = 'Báo cáo công nợ'
        app_label    = 'report'
