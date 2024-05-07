from rest_framework import permissions
from rest_framework.request import Request

from django.contrib.auth.models import PermissionsMixin

class DBPermissionsMixin(PermissionsMixin):
    def has_perm(self, perm, obj = None):
        super_perm = PermissionsMixin.has_perm(perm, obj)
        return super_perm or self.role.permissions.has_perm(perm)

class DBPermissionHandler(permissions.BasePermission):

    def __init__(self, db_permission):
        self.db_permision = db_permission

    def has_permission(self, request, view):

        if not request.user.is_authenticated: return False

        return request.user.has_perm(self.db_permision)