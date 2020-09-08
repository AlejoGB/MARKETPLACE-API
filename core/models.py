from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                     PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Se necesita email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, default=0)
    email = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=20, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    adress_1 = models.CharField(max_length=200, default=0)
    adress_2 = models.CharField(max_length=200, default=0)
    adress_3 = models.CharField(max_length=200, default=0)
    adress_4 = models.CharField(max_length=200, default=0)
    adress_5 = models.CharField(max_length=200, default=0)
    objects = UserManager()
    USERNAME_FIELD = 'email'
