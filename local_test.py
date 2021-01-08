"""
    Build a "local_test" YunoHost installation and start the Django dev. server against it.

    Run via:
        make local-test

    see README for details ;)
"""
import os
import subprocess
import sys
import time
from pathlib import Path

from django_ynh.test_utils import generate_basic_auth


try:
    from django_ynh.local_test import call_manage_py, create_local_test
except ImportError as err:
    raise ImportError('Did you forget to activate a virtual environment?') from err

BASE_PATH = Path(__file__).parent


def main():
    final_home_path = create_local_test(
        django_settings_path=BASE_PATH / 'conf' / 'settings.py',
        destination=BASE_PATH / 'local_test',
        runserver=False,
    )

    with Path(final_home_path / 'local_settings.py').open('a') as f:
        f.write('from huey import SqliteHuey\n')
        huey_db = final_home_path.parent / 'huey_db.sqlite'
        f.write(f'HUEY=SqliteHuey(filename="{huey_db}")\n')

    call_manage_py(final_home_path, 'makemigrations ci_ynh')
    call_manage_py(final_home_path, 'migrate --no-input')
    call_manage_py(final_home_path, 'collectstatic --no-input')
    call_manage_py(final_home_path, 'create_superuser --username="test"')

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    # All environment variables are passed to Django's "runnserver" ;)
    # "Simulate" SSOwat authentication, by set "http headers"
    # Still missing is the 'SSOwAuthUser' cookie,
    # but this is ignored, if settings.DEBUG=True ;)
    os.environ['HTTP_AUTH_USER'] = 'test'
    os.environ['HTTP_REMOTE_USER'] = 'test'

    os.environ['HTTP_AUTHORIZATION'] = generate_basic_auth(username='test', password='test123')

    huey_worker = subprocess.Popen(
        [sys.executable, 'manage.py', 'run_huey', '--worker-type=process', '--workers=2'],
        cwd=final_home_path,
    )
    time.sleep(0.5)
    assert huey_worker.poll() is None, 'Huey worker does not start?!?'

    try:
        try:
            call_manage_py(final_home_path, 'runserver')
        except KeyboardInterrupt:
            print('\nBye ;)')
    finally:
        huey_worker.terminate()
        time.sleep(1)
        huey_worker.kill()


if __name__ == '__main__':
    main()
