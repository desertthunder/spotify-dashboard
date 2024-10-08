"""API Model Mixins."""

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class TokenSetMixin(models.Model):
    """Token attributes."""

    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_expiry = models.DateTimeField()

    @property
    def token_expired(self) -> bool:
        """Check if the token is expired."""
        return True

    class Meta(TypedModelMeta):
        """TokenSet meta class."""

        abstract = True
