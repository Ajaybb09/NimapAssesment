from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
import uuid
from django.utils.translation import gettext_lazy as _
import jwt
from datetime import datetime,timedelta




class customerManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True, null=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now=True)
    Createdby = models.CharField(max_length=100 , null=True, blank=True)

    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = customerManager()

    @property
    def token(self):
        token = jwt.encode(
            {'id': self.id.hex,
             'email': self.email,
                # 'mobile': self.mobilenumber,
                'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')

        return token
 

    # def __str__(self):
    #     return self.Name




class EmployeeToken(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    Employee = models.CharField(max_length=255, null=True, blank=True)
    authToken = models.TextField(null=True, blank=True)
    isactive = models.BooleanField(default=True)


class Client(models.Model):
    client_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    Createdby = models.CharField(max_length=100 , null=True, blank=True)
    updated_at = models.DateTimeField(null = True)


class Project(models.Model):
    client_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    Createdby = models.CharField(max_length=100 , null=True, blank=True)
    updated_at = models.DateTimeField(null = True)
    user_id = models.ManyToManyField(Employee)
    project_name = models.CharField(max_length=255)

