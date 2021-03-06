from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView


# settings.PATH_URL is the $YNH_APP_ARG_PATH
# Prefix all urls with "PATH_URL":
urlpatterns = [
    path(f'{settings.PATH_URL}/', admin.site.urls),
]
if settings.PATH_URL:
    # redirect only, if we not installed in root domain level:
    urlpatterns.append(path('', RedirectView.as_view(pattern_name='admin:index')))
