from rest_framework import permissions
from rest_framework.request import Request

from django.contrib.auth import models as Models


from django.db import models

from django.utils.translation import gettext_lazy as _

class Role(Models.AbstractBaseUser, Models.PermissionsMixin):
    """User roles in the system"""

    groups = models.ManyToManyField(
        Models.Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="role_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Models.Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="role_set",
        related_query_name="user",
    )


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role_name = models.CharField(max_length=255, unique=True, primary_key=True)


class RolePermissionsMixin(Models.PermissionsMixin):
    
    class Meta:
        abstract = True

    role = models.ForeignKey(Role, on_delete=models.CASCADE, null = True, default=None)

    def has_perm(self, perm, obj = None):
        super_perm = super().has_perm(perm, obj)
        return super_perm or self.role.has_perm(perm, obj)


def getDBPermission(db_permission):

    class DBPermissionHandler(permissions.BasePermission):
        def __init__(self): 
            self.db_permission = db_permission

        def has_permission(self, request, view):
            if not request.user.is_authenticated: return False
            return request.user.has_perm(self.db_permission)

    return  DBPermissionHandler