import logging
from uuid import UUID

from huey import crontab
from huey.contrib.djhuey import lock_task, periodic_task, task

from ci_ynh.models import Check, Package
from ci_ynh.yunohost_utils import check_package


logger = logging.getLogger(__name__)


@periodic_task(
    crontab(minute='*'),  # run every minutes
    context=True,  # include the Task instance as a keyword argument
)
@lock_task('schedule_ci_pipeline')  # no multiple invocations from running concurrently
def schedule_ci_pipeline(task):
    qs = Package.objects.all()
    qs = qs.exclude(checks__status=Check.STATUS_RUNNING)
    for package in qs:
        logger.info('Schedule "%s"', package)
        ci_run(package_pk=package.pk)


@task(context=True)  # include the Task instance as a keyword argument
@lock_task('ci_run')  # no multiple invocations from running concurrently
def ci_run(*, package_pk, task):
    task_id = UUID(task.id)
    package = Package.objects.get(pk=package_pk)
    logger.info('CI run "%s"', package)
    check = Check.objects.create(package=package, task_id=task_id, status=Check.STATUS_RUNNING)

    check = check_package(package=package, check=check)
    logger.info('CI run "%s" done: %s', package, check)
