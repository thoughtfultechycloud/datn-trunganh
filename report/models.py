from django.db import models


class BaoCaoNoPT(models.Model):
    class Meta:
        managed             = False
        verbose_name        = 'Báo cáo nợ phải thu'
        verbose_name_plural = 'Báo cáo nợ phải thu'
        app_label           = 'report'


class BaoCaoNoPTra(models.Model):
    class Meta:
        managed             = False
        verbose_name        = 'Báo cáo nợ phải trả'
        verbose_name_plural = 'Báo cáo nợ phải trả'
        app_label           = 'report'


class BangKeChiTien(models.Model):
    class Meta:
        managed             = False
        verbose_name        = 'Bảng kê chi tiền'
        verbose_name_plural = 'Bảng kê chi tiền'
        app_label           = 'report'
