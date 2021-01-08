from bx_py_utils.models.timetracking import TimetrackingBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Package(TimetrackingBaseModel):
    """
    Store information about what project should be checked.
    """

    project_name = models.CharField(
        max_length=128,
        verbose_name=_('Package.project_name.verbose_name'),
        help_text=_('Package.project_name.help_text'),
    )
    url = models.URLField(
        # e.g.:
        # https://github.com/YunoHost-Apps/django_ynh/tree/master
        # https://github.com/YunoHost-Apps/django_ynh/tree/testing
        unique=True,
        verbose_name=_('Package.url.verbose_name'),
        help_text=_('Package.url.help_text'),
    )
    branch_name = models.CharField(
        # e.g.:
        # master
        # testing
        max_length=64,
        verbose_name=_('Package.branch_name.verbose_name'),
        help_text=_('Package.branch_name.help_text'),
    )
    args = models.TextField(
        # TODO: generate dynamically
        default='domain=domain.tld\npath=/path',
        verbose_name=_('Package.args.verbose_name'),
        help_text=_('Package.args.help_text'),
    )

    def get_args(self):
        args = []
        for line in str(self.args).splitlines():
            line = line.strip()
            if line:
                args.append(line)
        return '&'.join(args)

    def __str__(self):
        return f'{self.project_name} - {self.branch_name}'

    class Meta:
        verbose_name = _('Package')
        verbose_name_plural = _('Packages')


class Check(TimetrackingBaseModel):
    """
    Store information about a check run.
    """

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='checks',
        verbose_name=_('Check.package.verbose_name'),
        help_text=_('Check.package.help_text'),
    )
    task_id = models.UUIDField(
        editable=False, verbose_name=_('Check.task_id.verbose_name'), help_text=_('Check.task_id.help_text')
    )
    output = models.TextField(
        editable=False, verbose_name=_('Check.output.verbose_name'), help_text=_('Check.output.help_text')
    )

    STATUS_UNKNOWN = 'unknown'
    STATUS_RUNNING = 'running'
    STATUS_SUCCESS = 'success'
    STATUS_FAIL = 'fail'
    STATUS_CHOICES = (
        (STATUS_UNKNOWN, _('Unknown')),
        (STATUS_RUNNING, _('CI is Running')),
        (STATUS_SUCCESS, _('CI run successful')),
        (STATUS_FAIL, _('CI run failed')),
    )
    STATUS_CHOICES_DICT = dict(STATUS_CHOICES)
    STATUS_MAX_LENGTH = max(len(key) for key in STATUS_CHOICES_DICT.keys() if key is not None)

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=STATUS_MAX_LENGTH,
        default=STATUS_UNKNOWN,
        blank=True,
        null=True,
        editable=False,
        verbose_name=_('Check.status.verbose_name'),
        help_text=_('Check.status.help_text'),
    )

    def __str__(self):
        return f'{self.package} - {self.status}'

    class Meta:
        verbose_name = _('Pipeline status')
        verbose_name_plural = _('Pipeline status')
