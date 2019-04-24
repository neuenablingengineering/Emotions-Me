from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Profile(AbstractUser):

    username = models.CharField(max_length=255, unique=True, default="")
    email = models.EmailField(max_length=255, default="")
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")

    ACCOUNT_TYPE_CHOICES = (("STUDENT", "STUDENT"), ("TEACHER", "TEACHER"))

    account_type = models.CharField(max_length=7, choices=ACCOUNT_TYPE_CHOICES, default="STUDENT")
    # should only have data if ACCOUNT_TYPE = TEACHER
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="list_of_students")
    # should only have data if ACCOUNT_TYPE = STUDENT
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="list_of_teachers")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'account_type']
