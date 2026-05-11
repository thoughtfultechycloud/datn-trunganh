from django.db import models


class TTCongTy(models.Model):
    class Meta:
        managed             = False
        verbose_name        = 'TT công ty'
        verbose_name_plural = 'TT công ty'
        app_label           = 'info'


class HDSD(models.Model):
    class Meta:
        managed             = False
        verbose_name        = 'HDSD'
        verbose_name_plural = 'HDSD'
        app_label           = 'info'
