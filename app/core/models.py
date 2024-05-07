"""
Database models
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from core.permissions import DBPermissionsMixin

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Role(AbstractBaseUser, PermissionsMixin):
    """User roles in the system"""

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role_name = models.CharField(max_length=255, unique=True, primary_key=True)

    USERNAME_FIELD = 'role_name'


class LabAdmin(Role):
    """Lab Administrator role"""

    class Meta:
        permissions = [ ("lab_admin_creation", "Creation of lab admin users"),
                        ("lab_admin_modification", "Modification of lab admin users"),
                        ("assistant_inactivation", "Deletion of assistant users"),
                        ("assistant_modification", "Modification of assistant users"),
                        ("assistant_creation", "Creation of assistan users"),
                        ]
        proxy = True

    def save(self, *args, **kwargs):
        self.role_name = 'AdministradorLaboratorio'
        super.save(*args, **kwargs)

class LabAssistant(Role):
    """Lab Assistant role"""

    class Meta:
        permissions = []
        proxy = True

    def save(self, *args, **kwargs):
        self.role_name = 'AsistenteLaboratorio'
        super.save(*args, **kwargs)

class User(AbstractBaseUser, DBPermissionsMixin):
    """User in the system."""

    class Meta:
        permissions = [("own_password_modification", "Modification of self's account password"),
                       ("own_phone_modification", "Modification of self's account phone number"),]


    role = models.ForeignKey(Role, on_delete=models.CASCADE, null = True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'




class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title
