"""User model."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from api.models.mixins import TokenSetMixin


class AppUser(TokenSetMixin, AbstractUser):
    """Application User Model (Custom)."""

    public_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(blank=False, unique=True)

    username = None  # type: ignore
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta(TypedModelMeta):
        """Meta class for app user."""

        pass