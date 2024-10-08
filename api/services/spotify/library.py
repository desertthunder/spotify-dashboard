"""Spotify data service.

# TODO: Rename to library.
"""

import logging
import typing

import httpx

from api.libs.constants import SpotifyAPIEndpoints
from api.libs.exceptions import SpotifyAPIError

if typing.TYPE_CHECKING:
    from api.models import AppUser

logger = logging.getLogger("spotify_data_service")


class SpotifyLibraryService:
    """API actions for fetching data from the Spotify API."""

    def library_playlists(
        self, user: "AppUser", limit: int = 50, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's playlists."""
        yielded = 0
        next = f"{SpotifyAPIEndpoints.SavedPlaylists}"

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=next,
                params={"limit": limit},
            )

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            next = resp.get("next")

            if next is not None:
                next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

            if not all:
                yielded += len(resp.get("items"))

            yield from resp.get("items")

    def library_albums(
        self, user: "AppUser", limit: int = 50, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's albums."""
        yielded = 0
        next = f"{SpotifyAPIEndpoints.SavedAlbums}"

        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=next,
                params={"limit": limit},
            )

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            next = resp.get("next")

            if next is not None:
                next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

            if not all:
                yielded += len(resp.get("items"))

            yield from resp.get("items")

    def library_artists(
        self, user: "AppUser", limit: int = 50, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's followed artists."""
        yielded = 0
        next = f"{SpotifyAPIEndpoints.FollowedArtists}"
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            while next:
                if not all and yielded >= limit:
                    break

                response = client.get(
                    url=next,
                    params={"type": "artist", "limit": limit},
                )

                if response.is_error:
                    logger.error(f"Error: {response.text}")

                    raise SpotifyAPIError(response.text)

                resp = response.json()

                logger.debug(f"Response: {resp}")

                next = resp.get("artists", {}).get("next")

                if next is not None:
                    next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

                if not all:
                    yielded += len(resp.get("artists", {}).get("items"))

                yield from resp.get("artists", {}).get("items")

    def library_tracks(
        self, user: "AppUser", limit: int = 50, all: bool = False
    ) -> typing.Iterable[dict]:
        """Get the user's saved tracks."""
        yielded = 0
        next = f"{SpotifyAPIEndpoints.SavedTracks}"
        with httpx.Client(
            base_url=SpotifyAPIEndpoints.BASE_URL,
            headers={"Authorization": f"Bearer {user.access_token}"},
        ) as client:
            response = client.get(
                url=next,
                params={"limit": limit},
            )

            if response.is_error:
                logger.error(f"Error: {response.text}")

                raise SpotifyAPIError(response.text)

            resp = response.json()

            logger.debug(f"Response: {resp}")

            next = resp.get("next")

            if next is not None:
                next = next.replace(f"{SpotifyAPIEndpoints.BASE_URL}/", "")

            if not all:
                yielded += len(resp.get("items"))

            yield from resp.get("items")
