"""API Views."""

import logging
from http import HTTPMethod

import httpx
import jwt
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import redirect
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request as DRFRequest

from api.libs.constants import WEB_APP_URL, SpotifyAPIStates
from api.libs.exceptions import SpotifyAPIError
from api.libs.requests import RedirectURI
from api.libs.responses import (
    Album,
    Artist,
    Playlist,
    RecentlyPlayed,
    Track,
)
from api.models import AppUser
from api.models.permissions import SpotifyAuth, Token
from api.services.spotify import SpotifyAuthService, SpotifyDataService
from server import settings

default_auth_service = SpotifyAuthService()  # NOTE used for dependency injection
default_data_service = SpotifyDataService()  # NOTE used for dependency injection

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


class LoginView(views.APIView):
    """Login View."""

    auth_service: SpotifyAuthService

    def __init__(
        self, auth_service: SpotifyAuthService = default_auth_service, *args, **kwargs
    ) -> None:
        """Login View Constructor."""
        self.auth_service = auth_service

        super().__init__(*args, **kwargs)

    def get(self, request: DRFRequest) -> HttpResponse:
        """Spotify Callback.

        Endpoint: GET /api/login
        """
        logger.debug("Received a GET request to /api/login")

        authorization_code: str | None = request.query_params.get("code")
        state = request.query_params.get("state")

        if (
            state != SpotifyAPIStates.LOGIN
            or not authorization_code
            or request.query_params.get("error") is not None
        ):
            return HttpResponseForbidden()

        try:
            token_set = self.auth_service.get_access_token(authorization_code)
        except SpotifyAPIError as exc:
            logger.error(f"Spotify API Error details: {exc}")

            return HttpResponseBadRequest("Unable to get access token.")

        try:
            current_user = self.auth_service.get_current_user(token_set.access_token)
        except SpotifyAPIError as exc:
            logger.error(f"Spotify API Error details: {exc}")

            return HttpResponseBadRequest("Unable to get current user.")

        user = AppUser.objects.from_spotify(current_user, token_set)
        client_jwt = Token(user)

        client = httpx.Client(base_url=WEB_APP_URL)

        req = client.build_request(
            HTTPMethod.GET,
            url="/dashboard",
            params={"token": client_jwt.encode()},  # NOTE can be used to look up user.
        )

        resp = redirect(to=RedirectURI.from_request(req))
        resp.headers["Access-Control-Allow-Origin"] = "*"

        logger.debug("Redirecting to dashboard.")

        return resp

    def post(self, request: DRFRequest) -> HttpResponse:
        """Login to Spotify.

        Endpoint: POST /api/login
        """
        redirect_uri = self.auth_service.build_redirect_uri()

        resp = redirect(to=redirect_uri)
        resp.headers["Access-Control-Allow-Origin"] = "*"

        logger.debug("Redirecting to Spotify for login.")
        logger.debug(f"Headers: {resp.headers}")

        # TODO: Should this be a serialized response?
        return JsonResponse(data={"redirect": resp.url})


class ValidateView(views.APIView):
    """Validate View.

    Polled by the client to check if the JWT token is still valid.

    Endpoint: GET /api/validate
    """

    auth_service: SpotifyAuthService

    def __init__(
        self, auth_service: SpotifyAuthService = default_auth_service, *args, **kwargs
    ) -> None:
        """Validate View Constructor."""
        self.auth_service = auth_service

        super().__init__(*args, **kwargs)

    def post(self, request: DRFRequest) -> HttpResponse:
        """Validate the JWT token.

        Endpoint: GET /api/validate
        """
        token = request.headers.get("Authorization")

        if not token:
            return HttpResponseForbidden()

        tag, token = token.split(" ")
        if tag.lower() != "bearer":
            return HttpResponseForbidden()

        # TODO: Move to a validator class?
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            logger.debug(
                f"Invalid or expired token for user {payload.get('public_id')}"
            )
            return HttpResponseForbidden()

        logger.debug(f"Found token for user {payload.get('public_id')}")

        try:
            user = AppUser.objects.get(public_id=payload.get("public_id"))

            logger.debug(f"Found user: {user.public_id} with pk {user.pk}")
        except AppUser.DoesNotExist:
            logger.error("User not found.")

            return HttpResponseForbidden(content={"message": "User not found."})

        if user.token_expired:
            logger.debug("Token expired. Refreshing token.")

            try:
                success, updated_user = self.auth_service.refresh_access_token(
                    user.refresh_token
                )

                user = updated_user or user

                if not success:
                    return HttpResponseBadRequest("Unable to refresh token.")

                client_jwt = Token(user)

                return JsonResponse(
                    data={"message": "Updated token", "token": client_jwt.encode()}
                )
            except SpotifyAPIError as exc:
                logger.error(f"Spotify API Error details: {exc}")

                return HttpResponseBadRequest("Unable to refresh token.")

        return JsonResponse(data={"message": "Valid token.", "token": token})


class SpotifyDataView(views.APIView):
    """Base class for Spotify data views."""

    authentication_classes = [
        SpotifyAuth,
    ]
    permission_classes = [
        IsAuthenticated,
    ]

    data_service: SpotifyDataService

    def __init__(
        self, data_service: SpotifyDataService = default_data_service, *args, **kwargs
    ) -> None:
        """Validate View Constructor."""
        self.data_service = data_service

        super().__init__(*args, **kwargs)

    def get_user(self, request: DRFRequest) -> AppUser:
        """Get the user from the request."""
        return AppUser.objects.get(pk=request.user.pk)


class LastPlayedView(SpotifyDataView):
    """Get the last played track.

    Endpoint: GET /api/playback/last
    """

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the last played track.

        Endpoint: GET /api/playback/last
        """
        app_user = self.get_user(request)
        data = self.data_service.last_played(app_user)
        last_played = RecentlyPlayed.get(data[0])

        return JsonResponse(data=last_played.model_dump())


class RecentlyPlayedView(SpotifyDataView):
    """Get recently played tracks.

    Endpoint: GET /api/playback/recent
    """

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the last played track.

        Endpoint: GET /api/playback/last
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        data = self.data_service.recently_played(app_user, int(limit))
        recently_played = RecentlyPlayed.list(data)

        return JsonResponse({"data": [rp.model_dump() for rp in recently_played]})


class LibraryPlaylistsView(SpotifyDataView):
    """Get the user's playlists."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's playlists.

        Endpoint: GET /api/library/playlists
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        response = self.data_service.library_playlists(app_user, int(limit))
        data = Playlist.list(response)

        return JsonResponse(data={"data": [p.model_dump() for p in data]})


class LibraryArtistsView(SpotifyDataView):
    """Get the user's artists."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's artists.

        Endpoint: GET /api/library/artists
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        response = self.data_service.library_artists(app_user, int(limit))
        data = Artist.list(response)

        return JsonResponse(data={"data": [a.model_dump() for a in data]})


class LibraryAlbumsView(SpotifyDataView):
    """Get the user's albums."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's albums.

        Endpoint: GET /api/library/albums
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        response = self.data_service.library_albums(app_user, int(limit))
        data = Album.list(response)

        return JsonResponse(data={"data": [a.model_dump() for a in data]})


class LibraryTracksView(SpotifyDataView):
    """Get the user's tracks."""

    def get(self, request: DRFRequest) -> HttpResponse:
        """Get the user's tracks.

        Endpoint: GET /api/library/tracks
        """
        limit = request.query_params.get("limit", 5)
        app_user = self.get_user(request)
        response = self.data_service.library_tracks(app_user, int(limit))
        data = Track.list(response)
        return JsonResponse(data={"data": [t.model_dump() for t in data]})
