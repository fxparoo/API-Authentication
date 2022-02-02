from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email not set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have a is_staff=True field')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have a is_superuser=True field')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


ROLES = (
    ('Librarian', 'Librarian'),
    ('Teacher', 'Teacher'),
    ('Student', 'Student'),
)


class AppUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50, blank=False)
    class_name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(null=True)
    role = models.CharField(max_length=50, choices=ROLES, null=True)
    designation = models.CharField(max_length=50, null=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']
