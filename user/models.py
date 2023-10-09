from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=120)
    last_name = models.CharField(_("last name"), max_length=120)
    email = models.EmailField(_("email address"), unique=True)

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
