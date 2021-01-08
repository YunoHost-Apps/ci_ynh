from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ci_ynh.models import Check, Package
from ci_ynh.tasks import ci_run


def force_ci_run(modeladmin, request, queryset):
    class FakeTask:
        id = '00000000-1111-0000-0000-000000000001'

    for package in queryset:
        ci_run(package_pk=package.pk, task=FakeTask)


force_ci_run.short_description = _('Force CI run for selected entries')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    actions = [force_ci_run]


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    readonly_fields = ('task_id', 'output', 'status')
