import logging
import subprocess

from ci_ynh.models import Check, Package


logger = logging.getLogger(__name__)


def call_yunohost(*, action_name, args, package, check):
    logger.info('Start %r subprocess for "%s" with: %r', action_name, package, ' '.join(args))
    try:
        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=15 * 60,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as err:
        logger.exception('%s "%s" error: %s', action_name, package, err)
        check.status = Check.STATUS_FAIL
        check.output += f'\n{err.output}\n(return code: {err.returncode!r})'
        check.save()
        return check
    except subprocess.TimeoutExpired as err:
        logger.exception('%s "%s" timeout', action_name, package)
        check.status = Check.STATUS_FAIL
        check.output += f'\nTimeout ({err.timeout}sec.):\n{err.output}'
        check.save()
        return check

    returncode = process.returncode
    output = process.stdout
    if returncode != 0:
        logger.error('%s "%s" return code: %r', action_name, package, returncode)
        check.status = Check.STATUS_FAIL
        check.output += f'\n{action_name} failed:\n{output}\n(return code: {returncode!r})'
        check.save()
        return check

    check.output += f'\n{action_name} success:\n{output}\n(return code: {returncode!r})'
    check.save()

    return check


def check_package(*, package, check):
    assert isinstance(package, Package)
    assert isinstance(check, Check)

    args = (
        'sudo',
        'yunohost',
        'app',
        'install',
        package.url,
        '--label',
        f'{package.project_name}-{package.branch_name}',
        '--args',
        package.get_args(),
        '--force',  # Do not ask confirmation if the app is not safe to use
    )
    check = call_yunohost(action_name='install', args=args, package=package, check=check)
    if check.status is not Check.STATUS_RUNNING:
        # failed -> abort other steps
        return check

    args = (
        'sudo',
        'yunohost',
        'app',
        'remove',
        f'{package.project_name}-{package.branch_name}',
    )
    check = call_yunohost(action_name='remove', args=args, package=package, check=check)
    if check.status is not Check.STATUS_RUNNING:
        # failed -> abort other steps
        return check

    check.status = Check.STATUS_SUCCESS
    check.save()

    return check
