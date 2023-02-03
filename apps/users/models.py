from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import AuditModel


class User(AbstractUser):
    """
        Class for overwrite the django user default
    """
    pass


class Chef(AuditModel):
    """ Model for chefs """
    user = models.ForeignKey(
        User, 
        verbose_name=_('Chef´s user'),
        on_delete=models.PROTECT
    )
    name = models.CharField(
        max_length=150,
        verbose_name=_('Chef´s name'), 
        help_text=_('Full name of Chef')
    )
    nickname = models.CharField(
        max_length=24, 
        verbose_name=_('Nickname'), 
        help_text=_('Name to display in the interface')
    )
    description = models.CharField(
        max_length=400, 
        verbose_name=_('Short Description'), 
        help_text=_('Chef`s short description')
    )
    active = models.BooleanField(
        verbose_name=_('Is Active?'),
        default=True,
    )

    def __str__(self) -> str:
        return f'Chef: {self.nickname}'
