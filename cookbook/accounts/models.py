from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from cookbook.accounts.managers import CookbookUserManager
from cookbook.common.validators import name_contains_only_letters_validator


class CbUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = CookbookUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 20

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            name_contains_only_letters_validator,
        ]
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=[
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            name_contains_only_letters_validator,
        ]
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
    )

    cover_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
    )

    user = models.OneToOneField(
        CbUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_image(self):
        if self.image:
            return self.image.url
        return f'{settings.STATIC_URL}assets/img/profile-default.png'

    def get_cover_image(self):
        if self.cover_image:
            return self.cover_image.url
        return f'{settings.STATIC_URL}assets/img/Culinary-Hero.jpg'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
