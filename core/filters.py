"""Filterset Base Class."""

from django.db import models
from rest_framework.request import Request

from core.models import AppUser


class FilterMeta:
    """Metaclass for FilterSet."""

    default_queryset: models.QuerySet
    filter_fields: list[str] = []
    sort_fields: list[str] = []
    search_fields: list[str] = []


class FilterSet:
    """Filter queryset by fields available in the Playlist model."""

    def get_user(self, request: Request) -> AppUser:
        """Get the authenticated user."""
        user = request.user
        if isinstance(user, AppUser):
            return user
        else:
            raise ValueError("User is not authenticated.")

    def get_queryset(self, request: Request, *args, **kwargs) -> models.QuerySet:
        """Access initial queryset."""
        return self.Meta.default_queryset

    def __call__(
        self, request: Request, queryset: models.QuerySet | None = None, *args, **kwargs
    ) -> models.QuerySet:
        """Return the filtered queryset."""
        qs = self.get_queryset(request, queryset, *args, **kwargs)

        # Example: ?name=foo&public=true
        params = request.query_params.copy()

        # Example: ?sort=name&name_dir=desc
        sort_params = params.pop("sort", None)

        for key, value in params.items():
            if (
                key in self.Meta.filter_fields
                and (method := getattr(self, f"filter_{key}"))
                or key in self.Meta.search_fields
                and (method := getattr(self, f"search_{key}"))
            ):
                qs = method(qs, value, request)

        if sort_params:
            for key in sort_params:
                direction = params.pop(f"{key}_dir", "asc")
                if key in self.Meta.sort_fields and (
                    method := getattr(self, f"sort_{key}")
                ):
                    qs = method(qs, direction, request)

        return qs

    class Meta(FilterMeta):
        """Meta options."""

        pass
