"""Playlist Model."""

import datetime
import json
import typing
import uuid

import pydantic
from django.db import models
from django.utils import timezone
from django_stubs_ext.db.models import TypedModelMeta
from loguru import logger

from api.models.mixins import CanBeAnalyzedMixin
from api.models.music import SpotifyModel, TimestampedModel
from api.serializers import validation


class PlaylistSyncManager(models.Manager["Playlist"]):
    """Manager for syncing user playlists."""

    def clean_playlist(self, playlist: dict) -> validation.SyncPlaylist:
        """Clean playlist data."""
        try:
            owner = playlist.get("owner")
            version = playlist.get("snapshot_id")
            image_url = playlist.get("images", [{}])[0].get("url")
            public = playlist.get("public")
            shared = playlist.get("collaborative")
            name = playlist.get("name")
            spotify_id = playlist.get("id")

            if not owner:
                raise ValueError("Playlist has no owner.")
            elif not owner.get("id"):
                raise ValueError("Playlist owner has no id.")

            owner_id = owner.get("id")

            if not version:
                raise ValueError("Playlist has no version.")
            if not name or not spotify_id:
                raise ValueError("Playlist has no name or spotify_id (required).")

            data = {
                "name": name,
                "spotify_id": spotify_id,
                "owner_id": owner_id,
                "version": version,
                "image_url": image_url,
                "public": public,
                "shared": shared,
                "description": playlist.get("description"),
            }

            logger.info(f"Cleaned playlist: {data}")

            return validation.SyncPlaylist(**data)
        except (ValueError, pydantic.ValidationError) as e:
            logger.error(e)

            raise ValueError("Failed to validate playlist") from e

    def sync_playlist(self, cleaned: dict, user_pk: int) -> "Playlist":
        """Sync a single playlist."""
        data = validation.SyncPlaylist(**cleaned)
        playlist, _ = self.update_or_create(
            spotify_id=data.spotify_id,
            defaults={
                **data.model_dump(),
                "user_id": user_pk,
            },
        )

        if not playlist.version:
            logger.error(f"Data: {json.dumps(cleaned, indent=2)}")

            raise ValueError(
                f"Playlist {playlist.pk}:{playlist.spotify_id} has no version."
            )

        return playlist

    def complete_playlist_sync(self, playlist: "Playlist") -> uuid.UUID:
        """Complete playlist sync."""
        playlist.is_synced = True
        playlist.save()

        return playlist.pk

    def pre_sync(
        self, playlists: typing.Iterable[dict]
    ) -> list["validation.SyncPlaylist"]:
        """Validate API data and prepare for syncing."""
        result = []
        errored = []
        for playlist in playlists:
            try:
                result.append(
                    validation.SyncPlaylist(
                        name=playlist.get("name", ""),
                        spotify_id=playlist.get("id", ""),
                        owner_id=playlist.get("owner", {}).get("id"),
                        version=playlist.get("snapshot_id"),
                        image_url=playlist.get("images", [{}])[0].get("url"),
                        public=playlist.get("public"),
                        shared=playlist.get("collaborative"),
                        description=playlist.get("description"),
                    )
                )
            except (ValueError, pydantic.ValidationError) as e:
                logger.error(f"Failed to validate playlist: {playlist}. {e}")
                errored.append(playlist)
                continue

        logger.debug(f"Pre-synced {len(result)} playlists.")
        logger.debug(f"Errored {len(errored)} playlists")

        return result

    def do(
        self, playlists: list["validation.SyncPlaylist"], user_pk: int
    ) -> list["Playlist"]:
        """Batch create playlists.

        Returns list of tuple of playlist pks and spotify ids.
        """
        added: list[Playlist] = self.bulk_create(
            (
                self.model(**playlist.model_dump(), user_id=user_pk)
                for playlist in playlists
            ),
            ignore_conflicts=True,
        )

        logger.debug(f"Added {len(added)} playlists.")
        for playlist in added:
            logger.debug(f"Added playlist {playlist.pk} | {playlist.spotify_id}.")
        logger.debug([playlist.spotify_id for playlist in playlists])

        return list(
            self.filter(
                spotify_id__in=[playlist.spotify_id for playlist in playlists]
            ).all()
        )

    def complete_sync(
        self, library_pk: int, playlists: list["Playlist"]
    ) -> list[tuple[uuid.UUID, str]]:
        """Complete playlist sync.

        Sets is_synced to True and adds library to playlists.
        """
        updated = []

        for playlist in playlists:
            playlist.is_synced = True
            playlist.libraries.add(library_pk)
            playlist.save()

            logger.debug(f"Added playlist {playlist.pk} to library {library_pk}.")

            updated.append((playlist.pk, playlist.spotify_id))

        return updated


class Playlist(SpotifyModel, TimestampedModel, CanBeAnalyzedMixin):
    """Spotify playlist model.

    Required fields for creation:
        - name
        - spotify_id
        - owner_id

    Optional fields:
        - version
        - image_url
        - public
        - shared (i.e. collaborative)
        - description
    """

    version = models.CharField(max_length=255, blank=True, null=True)  # snapshot_id
    image_url = models.URLField(blank=True, null=True, max_length=1024)
    public = models.BooleanField(null=True, blank=True)
    shared = models.BooleanField(null=True, blank=True)  # collaborative
    description = models.TextField(blank=True, null=True)
    owner_id = models.CharField(max_length=255, null=False, blank=False)
    owner_name = models.CharField(max_length=255, null=True, blank=True)

    # (TODO): this should be a many-to-many relationship
    user = models.ForeignKey(
        "core.AppUser", related_name="playlists", on_delete=models.PROTECT, null=True
    )

    objects: models.Manager["Playlist"] = models.Manager()
    sync = PlaylistSyncManager()

    @property
    def stale_data(self) -> bool:
        """Check if playlist data is more than a week old."""
        return self.updated_at < timezone.now() - datetime.timedelta(days=7)

    @property
    def spotify_url(self) -> str:
        """Spotify URL for playlist."""
        return f"https://open.spotify.com/playlist/{self.spotify_id}"

    class Meta(TypedModelMeta):
        """Playlist model metadata."""

        ordering = ["-is_synced", "-is_analyzed", "-updated_at", "-created_at"]
        unique_together = ["spotify_id", "user"]
