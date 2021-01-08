from pathlib import Path

from django_ynh.path_utils import assert_is_file
from poetry_publish.publish import poetry_publish
from poetry_publish.utils.subprocess_utils import verbose_check_call

import ci_ynh


PACKAGE_ROOT = Path(ci_ynh.__file__).parent.parent.parent


def publish():
    """
    Publish to PyPi
    Call this via:
        $ make publish
    """
    assert_is_file(PACKAGE_ROOT / 'README.md')

    verbose_check_call('make', 'pytest')  # don't publish if tests fail

    poetry_publish(
        package_root=PACKAGE_ROOT,
        version=ci_ynh.__version__,
    )


if __name__ == '__main__':
    publish()
