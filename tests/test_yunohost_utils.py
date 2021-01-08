from uuid import UUID

from django.test import TestCase

from ci_ynh.models import Check, Package
from ci_ynh.yunohost_utils import check_package


class YunohostUtilsTestCase(TestCase):
    def test_check_package(self):
        package = Package.objects.create(
            project_name='django_ynh',
            url='https://github.com/YunoHost-Apps/django_ynh/tree/master',
            branch_name='master',
            args='domain=domain.tld\npath=/path',
        )
        check = Check.objects.create(
            package=package, task_id=UUID('00000000-1111-0000-0000-000000000001'), status=Check.STATUS_RUNNING
        )

        check = check_package(package=package, check=check)
        assert isinstance(check, Check)

        assert check.status == 'fail'
        assert 'return code:' in check.output
