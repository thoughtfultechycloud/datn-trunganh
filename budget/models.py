from django.contrib.auth.models import User
from django.db import models

from main.models import CostCategory, Project


class ProjectBudget(models.Model):
    STATUS_CHOICES = [
        ('Nhap',       'Nháp'),
        ('Cho_duyet',  'Chờ duyệt'),
        ('Da_duyet',   'Đã duyệt'),
    ]

    cost_category  = models.ForeignKey(CostCategory, on_delete=models.PROTECT, verbose_name='Hạng mục chi phí')
    project        = models.ForeignKey(Project, on_delete=models.PROTECT, verbose_name='Dự án')
    period         = models.CharField(max_length=10, verbose_name='Kỳ kế hoạch')
    planned_amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Ngân sách kế hoạch')
    actual_amount  = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name='Chi phí thực tế')
    approved_date  = models.DateField(null=True, blank=True, verbose_name='Ngày duyệt')
    approved_by    = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Người phê duyệt')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Nhap', verbose_name='Trạng thái')
    note           = models.CharField(max_length=300, blank=True, verbose_name='Ghi chú')

    class Meta:
        verbose_name        = 'Kế hoạch ngân sách'
        verbose_name_plural = 'Kế hoạch ngân sách dự án'
        ordering            = ['project', 'period', 'cost_category']
        unique_together     = [('cost_category', 'project', 'period')]

    def __str__(self):
        return f'{self.project} / {self.cost_category} / {self.period}'

    @property
    def variance(self):
        return self.planned_amount - self.actual_amount
