from django.db import models


class Backup(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Sao lưu dữ liệu'
        verbose_name_plural = 'Sao lưu dữ liệu'


class Restore(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Khôi phục dữ liệu'
        verbose_name_plural = 'Khôi phục dữ liệu'
