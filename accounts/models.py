from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

# Create your models here.

"""class Shopper(AbstractUser): 
    pass
""" 
class Shopper(AbstractUser):
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='shopper_set',   # Add a related_name argument here
        related_query_name='shopper'
    )
    groups = models.ManyToManyField(
    'auth.Group',
    verbose_name=_('groups'),
    blank=True,
    related_name='shopper_set',   # Add a related_name argument here
    related_query_name='shopper'
    )