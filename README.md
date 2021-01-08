# ci_ynh for YunoHost

[![Integration level](https://dash.yunohost.org/integration/ci_ynh.svg)](https://dash.yunohost.org/appci/app/ci_ynh) ![](https://ci-apps.yunohost.org/ci/badges/ci_ynh.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/ci_ynh.maintain.svg)
[![Install ci_ynh with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=ci_ynh)

> *This package allows you to install ci_ynh quickly and simply on a YunoHost server.
If you don't have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.*

**Experimental and currently not working ;)**

Pull requests welcome ;)

Discuss: https://forum.yunohost.org/t/ci-ynh-package-check-as-yunohost-app-using-django/13894

## Overview

[ci_ynh](https://github.comYunoHost-Apps/ci_ynh) CI to check YunoHost packages on self hosted YunoHost instance, using Python/Django.



## Links

 * Report a bugs: https://github.com/YunoHost-Apps/ci_ynh
 * YunoHost website: https://yunohost.org/

---

# Developer info

## package installation / debugging

Please send your pull request to https://github.com/YunoHost-Apps/ci_ynh

Try 'main' branch, e.g.:
```bash
sudo yunohost app install https://github.com/YunoHost-Apps/ci_ynh/tree/master --debug
or
sudo yunohost app upgrade ci_ynh -u https://github.com/YunoHost-Apps/ci_ynh/tree/master --debug
```

Try 'testing' branch, e.g.:
```bash
sudo yunohost app install https://github.com/YunoHost-Apps/ci_ynh/tree/testing --debug
or
sudo yunohost app upgrade ci_ynh -u https://github.com/YunoHost-Apps/ci_ynh/tree/testing --debug
```

To remove call e.g.:
```bash
sudo yunohost app remove ci_ynh
```

Run manual CI check. e.g.:
```bash
root@yunohost:~# cd /opt/yunohost/ci_ynh/
root@yunohost:/opt/yunohost/ci_ynh# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/ci_ynh# ./manage.py ci_run django_ynh
```

Backup / remove / restore cycle, e.g.:
```bash
yunohost backup create --apps ci_ynh
yunohost backup list
archives:
  - ci_ynh-pre-upgrade1
  - 20201223-163434
yunohost app remove ci_ynh
yunohost backup restore 20201223-163434 --apps ci_ynh
```

Debug installation, e.g.:
```bash
root@yunohost:~# ls -la /var/www/ci_ynh/
total 18
drwxr-xr-x 4 root root 4 Dec  8 08:36 .
drwxr-xr-x 6 root root 6 Dec  8 08:36 ..
drwxr-xr-x 2 root root 2 Dec  8 08:36 media
drwxr-xr-x 7 root root 8 Dec  8 08:40 static

root@yunohost:~# ls -la /opt/yunohost/ci_ynh/
total 58
drwxr-xr-x 5 ci_ynh ci_ynh   11 Dec  8 08:39 .
drwxr-xr-x 3 root        root           3 Dec  8 08:36 ..
-rw-r--r-- 1 ci_ynh ci_ynh  460 Dec  8 08:39 gunicorn.conf.py
-rw-r--r-- 1 ci_ynh ci_ynh    0 Dec  8 08:39 local_settings.py
-rwxr-xr-x 1 ci_ynh ci_ynh  274 Dec  8 08:39 manage.py
-rw-r--r-- 1 ci_ynh ci_ynh  171 Dec  8 08:39 secret.txt
drwxr-xr-x 6 ci_ynh ci_ynh    6 Dec  8 08:37 venv
-rw-r--r-- 1 ci_ynh ci_ynh  115 Dec  8 08:39 wsgi.py
-rw-r--r-- 1 ci_ynh ci_ynh 4737 Dec  8 08:39 settings.py

root@yunohost:~# cd /opt/yunohost/ci_ynh/
root@yunohost:/opt/yunohost/ci_ynh# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/ci_ynh# ./manage.py check
ci_ynh v0.8.2 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='settings'
PROJECT_PATH:/opt/yunohost/ci_ynh/venv/lib/python3.7/site-packages
BASE_PATH:/opt/yunohost/ci_ynh
System check identified no issues (0 silenced).

root@yunohost:~# tail -f /var/log/ci_ynh/ci_ynh.log
root@yunohost:~# cat /etc/systemd/system/ci_ynh.service

root@yunohost:~# systemctl reload-or-restart ci_ynh
root@yunohost:~# journalctl --unit=ci_ynh --follow
```

## local test

For quicker developing of ci_ynh in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone https://github.com/YunoHost-Apps/ci_ynh.git
~$ cd ci_ynh/
~/ci_ynh$ make
install-poetry         install or update poetry
install                install ci_ynh via poetry
update                 update the sources and installation
local-test             Run local_test.py to run ci_ynh locally
~/ci_ynh$ make install-poetry
~/ci_ynh$ make install
~/ci_ynh$ make local-test
```

Notes:

* SQlite database will be used
* A super user with username `test` and password `test` is created
* The page is available under `http://127.0.0.1:8000/app_path/`
