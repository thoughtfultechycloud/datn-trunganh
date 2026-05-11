from django.contrib import admin
from django.contrib.auth.models import User

from .models import ProjectBudget


@admin.register(ProjectBudget)
class ProjectBudgetAdmin(admin.ModelAdmin):
    list_display  = ('project', 'period', 'planned_amount', 'actual_amount', 'status', 'approved_by')
    list_filter   = ('status', 'project', 'period')
    search_fields = ('project__project_name', 'period')
    ordering      = ('project', 'period')
    readonly_fields = ('actual_amount',)
    radio_fields    = {'status': admin.HORIZONTAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'approved_by':
            kwargs['queryset'] = User.objects.filter(groups__name='Phê duyệt ngân sách').distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
