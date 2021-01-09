import huey_monitor
from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from huey_monitor.models import TaskModel

from ci_ynh.models import Check, Package
from ci_ynh.tasks import ci_run


def force_ci_run(modeladmin, request, queryset):
    for package in queryset:
        result = ci_run(package_pk=package.pk)
        messages.info(request, f'Task {result.id} scheduled')


force_ci_run.short_description = _('Force CI run for selected entries')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'ci_active', 'branch_name', 'update_dt')
    actions = [force_ci_run]


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    def task(self, obj):  # FIXME: Optimize DB queries ;)
        task_uuid = obj.task_id
        huey_monitor_task = TaskModel.objects.filter(task_id=task_uuid).first()
        if not huey_monitor_task:
            return task_uuid

        url = huey_monitor_task.admin_link()
        state = huey_monitor_task.state
        return format_html('<a href="{}">{}</a>', url, state)

    list_display = ('package', 'create_dt', 'update_dt', 'status', 'task')
    search_fields = ('package__project_name', 'task_id')
    readonly_fields = ('task_id', 'output', 'status')
    list_filter = ('status',)
    date_hierarchy = 'create_dt'
    ordering = ('-update_dt',)
