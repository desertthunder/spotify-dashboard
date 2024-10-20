"""Library serializers."""

from pydantic import BaseModel, Field

from api.models import Playlist as PlaylistModel
from api.serializers.base import Serializer


class Playlist(Serializer):
    """Playlist API response data."""

    spotify_id: str
    name: str
    owner_name: str
    owner_id: str
    link: str
    image_url: str
    num_tracks: int
    track_link: str
    version: str
    public: bool = False
    shared: bool = False
    description: str | None = None
    id: str | int | None = None
    is_synced: bool = False

    @classmethod
    def mappings(cls: type["Playlist"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "id",
            "name": "name",
            "version": "snapshot_id",
            "owner_name": "owner.display_name",
            "owner_id": "owner.id",
            "link": "external_urls.spotify",
            "image_url": "images.0.url",
            "num_tracks": "tracks.total",
            "track_link": "tracks.href",
        }

    @classmethod
    def nullable_fields(cls: type["Playlist"]) -> tuple:
        """Fields that can be null."""
        return (
            "description",
            "public",
            "collaborative",
        )

    @classmethod
    def get(cls: type["Playlist"], response: dict) -> "Playlist":
        """Create a Playlist object from JSON data."""
        data = cls.map_response(response)

        is_public = response.get("public")
        is_shared = response.get("collaborative")

        if is_public == "":
            data["public"] = False
        elif is_public is not None:
            data["public"] = is_public

        if is_shared == "":
            data["shared"] = False
        elif is_shared is not None:
            data["shared"] = is_shared

        if record := PlaylistModel.objects.filter(
            spotify_id=data["spotify_id"]
        ).first():
            data["is_synced"] = record.is_synced
            data["id"] = str(record.id)

        return cls(**data)


class PlaylistTrack(BaseModel):
    """Playlist track serializer."""

    # track.id
    spotify_id: str
    # track.name
    name: str
    # album.id
    album_id: str
    # album.name
    album_name: str
    # album.album_type
    album_type: str
    # artists[].id, artists[].name
    artists: list[tuple[str, str]]
    # duration_ms
    duration_ms: int
    # external_ids.isrc
    isrc: str | None = None


class ExpandedPlaylist(BaseModel):
    """Expanded playlist serializer."""

    # id
    spotify_id: str
    collaborative: bool
    description: str
    # external_urls.spotify
    spotify_link: str
    # images.0.url
    image_url: str
    name: str
    # owner.id, owner.display_name
    owner: tuple[str, str]
    public: bool
    snapshot_id: str
    # followers.total
    follower_count: int
    id: str | int | None = None

    tracks: list[PlaylistTrack] = Field(default_factory=list)

    @classmethod
    def get(cls: type["ExpandedPlaylist"], response: dict) -> "ExpandedPlaylist":
        """Create an ExpandedPlaylist object from JSON data."""
        playlist: ExpandedPlaylist = ExpandedPlaylist.model_construct()

        if playlist_data := response.get("playlist"):
            playlist = ExpandedPlaylist(
                spotify_id=playlist_data.get("id"),
                collaborative=playlist_data.get("collaborative"),
                description=playlist_data.get("description"),
                spotify_link=playlist_data.get("external_urls", {}).get("spotify"),
                image_url=playlist_data.get("images", [{}])[0].get("url"),
                name=playlist_data.get("name"),
                owner=(
                    playlist_data.get("owner", {}).get("id"),
                    playlist_data.get("owner", {}).get("display_name"),
                ),
                public=playlist_data.get("public"),
                snapshot_id=playlist_data.get("snapshot_id"),
                follower_count=playlist_data.get("followers", {}).get("total"),
                tracks=[],
            )
        else:
            raise ValueError("Invalid playlist data.")

        tracks: list[PlaylistTrack] = []

        if track_data := response.get("tracks"):
            for item in track_data:
                item = item.get("track", {})
                track_data = item.get("track", {})

                artists = [
                    (artist.get("id", ""), artist.get("name", ""))
                    for artist in item.get("artists", [])
                ]
                tracks.append(
                    PlaylistTrack(
                        spotify_id=item.get("id"),
                        name=item.get("name"),
                        album_id=item.get("album", {}).get("id"),
                        album_name=item.get("album", {}).get("name"),
                        album_type=item.get("album", {}).get("album_type"),
                        artists=artists,
                        duration_ms=item.get("duration_ms"),
                        isrc=item.get("external_ids", {}).get("isrc"),
                    )
                )

        playlist.tracks.extend(tracks)

        if record := PlaylistModel.objects.filter(
            spotify_id=playlist.spotify_id
        ).first():
            playlist.id = str(record.id)

        return playlist


class Album(Serializer):
    """Album API response data."""

    spotify_id: str
    name: str
    artist_name: str
    artist_id: str
    release_date: str
    total_tracks: int
    image_url: str
    label: str | None = None
    genres: list[str] | None = None

    @classmethod
    def mappings(cls: type["Album"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "album.id",
            "name": "album.name",
            "artist_name": "album.artists.0.name",
            "artist_id": "album.artists.0.id",
            "release_date": "album.release_date",
            "total_tracks": "album.total_tracks",
            "image_url": "album.images.0.url",
        }

    @classmethod
    def nullable_fields(cls: type["Album"]) -> tuple:
        """Fields that can be null."""
        return (
            "label",
            "genres",
        )


class Track(Serializer):
    """Track API response data."""

    spotify_id: str
    name: str
    artist_name: str
    artist_id: str
    album_name: str
    album_id: str
    image_url: str
    duration_ms: int
    link: str

    @classmethod
    def mappings(cls: type["Track"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "spotify_id": "track.id",
            "name": "track.name",
            "artist_name": "track.artists.0.name",
            "artist_id": "track.artists.0.id",
            "album_name": "track.album.name",
            "album_id": "track.album.id",
            "image_url": "track.album.images.0.url",
            "duration_ms": "track.duration_ms",
            "link": "track.external_urls.spotify",
        }

    @classmethod
    def nullable_fields(cls: type["Track"]) -> tuple:
        """Fields that can be null."""
        return ("",)


class Artist(Serializer):
    """Artist API response data."""

    genres: list[str]
    spotify_id: str
    name: str
    link: str
    image_url: str

    @classmethod
    def mappings(cls: type["Artist"]) -> dict[str, str]:
        """Mapping of JSON data to class properties."""
        return {
            "genres": "genres",
            "spotify_id": "id",
            "name": "name",
            "link": "external_urls.spotify",
            "image_url": "images.0.url",
        }

    @classmethod
    def nullable_fields(cls: type["Artist"]) -> tuple:
        """Fields that can be null."""
        return ("",)
