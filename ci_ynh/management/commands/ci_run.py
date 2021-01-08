import sys
from uuid import UUID

from django.core.management.base import BaseCommand

from ci_ynh.models import Check, Package
from ci_ynh.yunohost_utils import check_package


class Command(BaseCommand):
    help = 'Start a CI run in foreground'

    def add_arguments(self, parser):
        parser.add_argument('project_name')

    def handle(self, *args, **options):
        project_name = options['project_name']
        print(f'Start CI run for project: {project_name!r}...')

        package = Package.objects.filter(project_name=project_name).first()
        if package is None:
            print(f'ERROR: project name {project_name!r} does not exists!')
            print('Registered names are:')
            names = Package.objects.values_list('project_name', flat=True)
            for name in names:
                print(f' * {name!r}')
            sys.exit(-1)

        print(package)
        check = Check.objects.create(
            package=package, task_id=UUID('00000000-1111-0000-0000-000000000001'), status=Check.STATUS_RUNNING
        )

        check = check_package(package=package, check=check)
        print(f'CI run "{package}" done: {check}')
