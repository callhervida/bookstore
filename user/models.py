from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        AUTHOR = "AUTHOR", 'Author'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    email = models.EmailField(unique=True)
    national_code = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True)
    profile_picture = models.FileField(blank=True, null=True)
    is_author = models.BooleanField(default=False)
    # username = phone_number

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class Author(User):
    base_role = User.Role.AUTHOR

    class Meta:
        proxy = True