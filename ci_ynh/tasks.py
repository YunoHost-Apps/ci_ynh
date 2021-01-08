import datetime
import logging
from uuid import UUID

from django.utils import timezone
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
    """
    Schedule activate packages for a CI run
    """
    # Set outdated checks to timeout:
    qs = Check.objects.filter(status=Check.STATUS_RUNNING)
    qs = qs.filter(update_dt__lt=timezone.now() - datetime.timedelta(minutes=30))
    qs.update(status=Check.STATUS_TIMEOUT)

    # Get all active and not running packages:
    qs = Package.objects.filter(ci_active=True)
    qs = qs.exclude(checks__status=Check.STATUS_RUNNING)

    # TODO: Order oldest CI run to first

    # Schedule filtered packages:
    for package in qs:
        logger.info('Schedule "%s"', package)
        ci_run(package_pk=package.pk)


@task(context=True)  # include the Task instance as a keyword argument
@lock_task('ci_run')  # no multiple invocations from running concurrently
def ci_run(*, package_pk, task):
    """
    CI run for one package
    """
    task_id = UUID(task.id)
    package = Package.objects.get(pk=package_pk)

    if package.ci_active is not True:
        # Should not happen
        logger.warning('Skip deactivated package: "%s"', package)
        return

    logger.info('CI run "%s"', package)
    check = Check.objects.create(package=package, task_id=task_id, status=Check.STATUS_RUNNING)

    check = check_package(package=package, check=check)
    logger.info('CI run "%s" done: %s', package, check)
