# Sync

From the sync process, we fetch playlist data to store in the database.

1. `playlist.items` for Tracks
    - Extracted Fields: `id`, `name`, `duration_ms`, `album`, `artists`
2. `playlist.items[].track.artists` for Artists
    - Extracted Fields: `id`, `name`
3. `playlist.items[].track.album` for Albums
    - Extracted Fields: `id`, `name`, `release_date`, `images`, `artists`

Since there is likely overlap between the artists and album artists, the strategy
is to create two dictionaries for each set and then merge them.

```python
{
    "{artist_id}": {
        "id": "{artist_id}",
        "name": "{artist_name}"
    },
}

combined = {**track_artists, **album_artists}

```

## Demo

In order to setup the demo and view some of my playlists' information, I ran this
query on my data:

```python
me = AppUser.objects.get(spotify_id="my-spotify-id")

# Spotify Wrapped playlists are titled 'Your Top Songs 20XX'
playlists = Playlist.objects.filter(name__icontains="your top songs") \
              .all()
sids = playlists.values_list("spotify_id", flat=True)
pks = playlists.values_list("id", flat=True)

tasks = [
  chain(sync_playlist_tasks.s(sid, me.pk), \
    sync_track_analysis_for_playlist.s(me.pk)) \
      for sid in sids
]

for task in tasks:
  task.apply_async()
  time.sleep(5)
```

## Mappings

| Model | Spotify Field | Internal Field | Required? |
| --- | --- | --- | --- |
| Track | `playlist.items[].track.id` | `spotify_id` | Yes |
|       | `playlist.items[].track.name` | `name` | Yes |
|       | `playlist.items[].track.duration_ms` | `duration` | No |
| Album | `playlist.items[].track.album.id` | `spotify_id` | Yes |
|       | `playlist.items[].track.album.name` | `name` | Yes |
|       | `playlist.items[].track.album.release_date` | `release_year` | No |
|       | `playlist.items[].track.album.images[].url` | `image_url` | No |
|       | `playlist.items[].track.album.artists[].id` | `album_type` | No |

```json
{
  "href": "https://api.spotify.com/v1/playlists/0bvQqiccwgkyu0lktmklS4/tracks?offset=0&limit=100&locale=en-US,en;q%3D0.9",
  "items": [
    {
      "added_at": "2024-10-04T13:35:25Z",
      "added_by": {
        "external_urls": {
          "spotify": "https://open.spotify.com/user/browais"
        },
        "href": "https://api.spotify.com/v1/users/browais",
        "id": "browais",
        "type": "user",
        "uri": "spotify:user:browais"
      },
      "is_local": false,
      "primary_color": null,
      "track": {
        "preview_url": "https://p.scdn.co/mp3-preview/82b453f5d78ed330e0b52f5a6d31f9600fe623ba?cid=cfe923b2d660439caf2b557b21f31221",
        "explicit": false,
        "type": "track",
        "episode": false,
        "track": true,
        "album": {
          "type": "album",
          "album_type": "album",
          "href": "https://api.spotify.com/v1/albums/7ylxV9GzV7U6lhQLKnHGWU",
          "id": "7ylxV9GzV7U6lhQLKnHGWU",
          "images": [
            {
              "height": 640,
              "url": "https://i.scdn.co/image/ab67616d0000b27340af56f52454ea6249d47a0d",
              "width": 640
            },
            {
              "height": 300,
              "url": "https://i.scdn.co/image/ab67616d00001e0240af56f52454ea6249d47a0d",
              "width": 300
            },
            {
              "height": 64,
              "url": "https://i.scdn.co/image/ab67616d0000485140af56f52454ea6249d47a0d",
              "width": 64
            }
          ],
          "name": "MOBILE SUIT GUNDAM UNICORN Original Motion Picture Soundtrack 1",
          "release_date": "2010-09-09",
          "release_date_precision": "day",
          "uri": "spotify:album:7ylxV9GzV7U6lhQLKnHGWU",
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/0Riv2KnFcLZA3JSVryRg4y"
              },
              "href": "https://api.spotify.com/v1/artists/0Riv2KnFcLZA3JSVryRg4y",
              "id": "0Riv2KnFcLZA3JSVryRg4y",
              "name": "Hiroyuki Sawano",
              "type": "artist",
              "uri": "spotify:artist:0Riv2KnFcLZA3JSVryRg4y"
            },
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/3gMQIwIzRRTX8tQg5COTaX"
              },
              "href": "https://api.spotify.com/v1/artists/3gMQIwIzRRTX8tQg5COTaX",
              "id": "3gMQIwIzRRTX8tQg5COTaX",
              "name": "Cyua",
              "type": "artist",
              "uri": "spotify:artist:3gMQIwIzRRTX8tQg5COTaX"
            },
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/34Dk2YNEZKcrTrUd6GIjFt"
              },
              "href": "https://api.spotify.com/v1/artists/34Dk2YNEZKcrTrUd6GIjFt",
              "id": "34Dk2YNEZKcrTrUd6GIjFt",
              "name": "Yumiko Inoue",
              "type": "artist",
              "uri": "spotify:artist:34Dk2YNEZKcrTrUd6GIjFt"
            }
          ],
          "external_urls": {
            "spotify": "https://open.spotify.com/album/7ylxV9GzV7U6lhQLKnHGWU"
          },
          "total_tracks": 24
        },
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/0Riv2KnFcLZA3JSVryRg4y"
            },
            "href": "https://api.spotify.com/v1/artists/0Riv2KnFcLZA3JSVryRg4y",
            "id": "0Riv2KnFcLZA3JSVryRg4y",
            "name": "Hiroyuki Sawano",
            "type": "artist",
            "uri": "spotify:artist:0Riv2KnFcLZA3JSVryRg4y"
          }
        ],
        "disc_number": 1,
        "track_number": 4,
        "duration_ms": 125858,
        "external_ids": {
          "isrc": "JPP301000064"
        },
        "external_urls": {
          "spotify": "https://open.spotify.com/track/0EnuLKOAs50ImBtBhKrh4U"
        },
        "href": "https://api.spotify.com/v1/tracks/0EnuLKOAs50ImBtBhKrh4U",
        "id": "0EnuLKOAs50ImBtBhKrh4U",
        "name": "Mineva",
        "popularity": 19,
        "uri": "spotify:track:0EnuLKOAs50ImBtBhKrh4U",
        "is_local": false
      },
      "video_thumbnail": {
        "url": null
      }
    },
    {
      "added_at": "2024-10-04T13:39:51Z",
      "added_by": {
        "external_urls": {
          "spotify": "https://open.spotify.com/user/browais"
        },
        "href": "https://api.spotify.com/v1/users/browais",
        "id": "browais",
        "type": "user",
        "uri": "spotify:user:browais"
      },
      "is_local": false,
      "primary_color": null,
      "track": {
        "preview_url": "https://p.scdn.co/mp3-preview/05751a349e5fdd71e2402e2b33242ae64bf3f44e?cid=cfe923b2d660439caf2b557b21f31221",
        "explicit": false,
        "type": "track",
        "episode": false,
        "track": true,
        "album": {
          "type": "album",
          "album_type": "single",
          "href": "https://api.spotify.com/v1/albums/44y4l05ZVogoQNZy2OHFxg",
          "id": "44y4l05ZVogoQNZy2OHFxg",
          "images": [
            {
              "height": 640,
              "url": "https://i.scdn.co/image/ab67616d0000b2738bffb0b0754bd36742d49e69",
              "width": 640
            },
            {
              "height": 300,
              "url": "https://i.scdn.co/image/ab67616d00001e028bffb0b0754bd36742d49e69",
              "width": 300
            },
            {
              "height": 64,
              "url": "https://i.scdn.co/image/ab67616d000048518bffb0b0754bd36742d49e69",
              "width": 64
            }
          ],
          "name": "Got Boost？ - TV size（『仮面ライダーガヴ』主題歌）",
          "release_date": "2024-09-01",
          "release_date_precision": "day",
          "uri": "spotify:album:44y4l05ZVogoQNZy2OHFxg",
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/162Ols90jU4CctXQz15NxS"
              },
              "href": "https://api.spotify.com/v1/artists/162Ols90jU4CctXQz15NxS",
              "id": "162Ols90jU4CctXQz15NxS",
              "name": "FANTASTICS from EXILE TRIBE",
              "type": "artist",
              "uri": "spotify:artist:162Ols90jU4CctXQz15NxS"
            }
          ],
          "external_urls": {
            "spotify": "https://open.spotify.com/album/44y4l05ZVogoQNZy2OHFxg"
          },
          "total_tracks": 1
        },
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/162Ols90jU4CctXQz15NxS"
            },
            "href": "https://api.spotify.com/v1/artists/162Ols90jU4CctXQz15NxS",
            "id": "162Ols90jU4CctXQz15NxS",
            "name": "FANTASTICS from EXILE TRIBE",
            "type": "artist",
            "uri": "spotify:artist:162Ols90jU4CctXQz15NxS"
          }
        ],
        "disc_number": 1,
        "track_number": 1,
        "duration_ms": 79300,
        "external_ids": {
          "isrc": "JPB602402708"
        },
        "external_urls": {
          "spotify": "https://open.spotify.com/track/2FwEI1ZNbKqpRDuKDn6JWk"
        },
        "href": "https://api.spotify.com/v1/tracks/2FwEI1ZNbKqpRDuKDn6JWk",
        "id": "2FwEI1ZNbKqpRDuKDn6JWk",
        "name": "Got Boost？ - TV size（『仮面ライダーガヴ』主題歌）",
        "popularity": 53,
        "uri": "spotify:track:2FwEI1ZNbKqpRDuKDn6JWk",
        "is_local": false
      },
      "video_thumbnail": {
        "url": null
      }
    },
    {
      "added_at": "2024-10-05T21:21:09Z",
      "added_by": {
        "external_urls": {
          "spotify": "https://open.spotify.com/user/browais"
        },
        "href": "https://api.spotify.com/v1/users/browais",
        "id": "browais",
        "type": "user",
        "uri": "spotify:user:browais"
      },
      "is_local": false,
      "primary_color": null,
      "track": {
        "preview_url": "https://p.scdn.co/mp3-preview/8230ef758c6855adca0b49175ded56e6d07d8b82?cid=cfe923b2d660439caf2b557b21f31221",
        "explicit": false,
        "type": "track",
        "episode": false,
        "track": true,
        "album": {
          "type": "album",
          "album_type": "album",
          "href": "https://api.spotify.com/v1/albums/17ZzUupJuP54aPsWn7eCKb",
          "id": "17ZzUupJuP54aPsWn7eCKb",
          "images": [
            {
              "height": 640,
              "url": "https://i.scdn.co/image/ab67616d0000b273b8bf4d447ecc2c7914cb791c",
              "width": 640
            },
            {
              "height": 300,
              "url": "https://i.scdn.co/image/ab67616d00001e02b8bf4d447ecc2c7914cb791c",
              "width": 300
            },
            {
              "height": 64,
              "url": "https://i.scdn.co/image/ab67616d00004851b8bf4d447ecc2c7914cb791c",
              "width": 64
            }
          ],
          "name": "orbital period",
          "release_date": "2007-12-19",
          "release_date_precision": "day",
          "uri": "spotify:album:17ZzUupJuP54aPsWn7eCKb",
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/0hSFeqPehe7FtCNWuQ6Bsy"
              },
              "href": "https://api.spotify.com/v1/artists/0hSFeqPehe7FtCNWuQ6Bsy",
              "id": "0hSFeqPehe7FtCNWuQ6Bsy",
              "name": "BUMP OF CHICKEN",
              "type": "artist",
              "uri": "spotify:artist:0hSFeqPehe7FtCNWuQ6Bsy"
            }
          ],
          "external_urls": {
            "spotify": "https://open.spotify.com/album/17ZzUupJuP54aPsWn7eCKb"
          },
          "total_tracks": 17
        },
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/0hSFeqPehe7FtCNWuQ6Bsy"
            },
            "href": "https://api.spotify.com/v1/artists/0hSFeqPehe7FtCNWuQ6Bsy",
            "id": "0hSFeqPehe7FtCNWuQ6Bsy",
            "name": "BUMP OF CHICKEN",
            "type": "artist",
            "uri": "spotify:artist:0hSFeqPehe7FtCNWuQ6Bsy"
          }
        ],
        "disc_number": 1,
        "track_number": 3,
        "duration_ms": 334613,
        "external_ids": {
          "isrc": "JPTF00707501"
        },
        "external_urls": {
          "spotify": "https://open.spotify.com/track/6QzCdBKoj7OH6RdPtK8psW"
        },
        "href": "https://api.spotify.com/v1/tracks/6QzCdBKoj7OH6RdPtK8psW",
        "id": "6QzCdBKoj7OH6RdPtK8psW",
        "name": "メーデー",
        "popularity": 45,
        "uri": "spotify:track:6QzCdBKoj7OH6RdPtK8psW",
        "is_local": false
      },
      "video_thumbnail": {
        "url": null
      }
    },
    {
      "added_at": "2024-10-08T13:06:18Z",
      "added_by": {
        "external_urls": {
          "spotify": "https://open.spotify.com/user/browais"
        },
        "href": "https://api.spotify.com/v1/users/browais",
        "id": "browais",
        "type": "user",
        "uri": "spotify:user:browais"
      },
      "is_local": false,
      "primary_color": null,
      "track": {
        "preview_url": "https://p.scdn.co/mp3-preview/c6549abc86f7da1fae4f8348198da78bc21674bf?cid=cfe923b2d660439caf2b557b21f31221",
        "explicit": false,
        "type": "track",
        "episode": false,
        "track": true,
        "album": {
          "type": "album",
          "album_type": "single",
          "href": "https://api.spotify.com/v1/albums/1xml9CR90tJdvTESDk4Q4s",
          "id": "1xml9CR90tJdvTESDk4Q4s",
          "images": [
            {
              "height": 640,
              "url": "https://i.scdn.co/image/ab67616d0000b273cb6080eae6c43b7ed1bb44b4",
              "width": 640
            },
            {
              "height": 300,
              "url": "https://i.scdn.co/image/ab67616d00001e02cb6080eae6c43b7ed1bb44b4",
              "width": 300
            },
            {
              "height": 64,
              "url": "https://i.scdn.co/image/ab67616d00004851cb6080eae6c43b7ed1bb44b4",
              "width": 64
            }
          ],
          "name": "絆ノ奇跡",
          "release_date": "2023-04-10",
          "release_date_precision": "day",
          "uri": "spotify:album:1xml9CR90tJdvTESDk4Q4s",
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/3NTbOmzlj2cL86XFuDVFvZ"
              },
              "href": "https://api.spotify.com/v1/artists/3NTbOmzlj2cL86XFuDVFvZ",
              "id": "3NTbOmzlj2cL86XFuDVFvZ",
              "name": "MAN WITH A MISSION",
              "type": "artist",
              "uri": "spotify:artist:3NTbOmzlj2cL86XFuDVFvZ"
            },
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/45ft4DyTCEJfQwTBHXpdhM"
              },
              "href": "https://api.spotify.com/v1/artists/45ft4DyTCEJfQwTBHXpdhM",
              "id": "45ft4DyTCEJfQwTBHXpdhM",
              "name": "milet",
              "type": "artist",
              "uri": "spotify:artist:45ft4DyTCEJfQwTBHXpdhM"
            }
          ],
          "external_urls": {
            "spotify": "https://open.spotify.com/album/1xml9CR90tJdvTESDk4Q4s"
          },
          "total_tracks": 1
        },
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/3NTbOmzlj2cL86XFuDVFvZ"
            },
            "href": "https://api.spotify.com/v1/artists/3NTbOmzlj2cL86XFuDVFvZ",
            "id": "3NTbOmzlj2cL86XFuDVFvZ",
            "name": "MAN WITH A MISSION",
            "type": "artist",
            "uri": "spotify:artist:3NTbOmzlj2cL86XFuDVFvZ"
          },
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/45ft4DyTCEJfQwTBHXpdhM"
            },
            "href": "https://api.spotify.com/v1/artists/45ft4DyTCEJfQwTBHXpdhM",
            "id": "45ft4DyTCEJfQwTBHXpdhM",
            "name": "milet",
            "type": "artist",
            "uri": "spotify:artist:45ft4DyTCEJfQwTBHXpdhM"
          }
        ],
        "disc_number": 1,
        "track_number": 1,
        "duration_ms": 223320,
        "external_ids": {
          "isrc": "JPU902300267"
        },
        "external_urls": {
          "spotify": "https://open.spotify.com/track/2VBLFxCUyFp5BfmsZpxcis"
        },
        "href": "https://api.spotify.com/v1/tracks/2VBLFxCUyFp5BfmsZpxcis",
        "id": "2VBLFxCUyFp5BfmsZpxcis",
        "name": "絆ノ奇跡",
        "popularity": 68,
        "uri": "spotify:track:2VBLFxCUyFp5BfmsZpxcis",
        "is_local": false
      },
      "video_thumbnail": {
        "url": null
      }
    },
    {
      "added_at": "2024-10-08T13:21:48Z",
      "added_by": {
        "external_urls": {
          "spotify": "https://open.spotify.com/user/browais"
        },
        "href": "https://api.spotify.com/v1/users/browais",
        "id": "browais",
        "type": "user",
        "uri": "spotify:user:browais"
      },
      "is_local": false,
      "primary_color": null,
      "track": {
        "preview_url": "https://p.scdn.co/mp3-preview/12b76cbff6bc7fe4e41e4a0a4f7803e18d8575d8?cid=cfe923b2d660439caf2b557b21f31221",
        "explicit": false,
        "type": "track",
        "episode": false,
        "track": true,
        "album": {
          "type": "album",
          "album_type": "single",
          "href": "https://api.spotify.com/v1/albums/1GF6yKJM4ovwW2zJUCMwgg",
          "id": "1GF6yKJM4ovwW2zJUCMwgg",
          "images": [
            {
              "height": 640,
              "url": "https://i.scdn.co/image/ab67616d0000b2738d674a890ce2fcd3d3ef2fd9",
              "width": 640
            },
            {
              "height": 300,
              "url": "https://i.scdn.co/image/ab67616d00001e028d674a890ce2fcd3d3ef2fd9",
              "width": 300
            },
            {
              "height": 64,
              "url": "https://i.scdn.co/image/ab67616d000048518d674a890ce2fcd3d3ef2fd9",
              "width": 64
            }
          ],
          "name": "⚡️",
          "release_date": "2024-07-17",
          "release_date_precision": "day",
          "uri": "spotify:album:1GF6yKJM4ovwW2zJUCMwgg",
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/32k7rSC70F3C7qif9Pgavi"
              },
              "href": "https://api.spotify.com/v1/artists/32k7rSC70F3C7qif9Pgavi",
              "id": "32k7rSC70F3C7qif9Pgavi",
              "name": "Humbreaders",
              "type": "artist",
              "uri": "spotify:artist:32k7rSC70F3C7qif9Pgavi"
            }
          ],
          "external_urls": {
            "spotify": "https://open.spotify.com/album/1GF6yKJM4ovwW2zJUCMwgg"
          },
          "total_tracks": 1
        },
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/32k7rSC70F3C7qif9Pgavi"
            },
            "href": "https://api.spotify.com/v1/artists/32k7rSC70F3C7qif9Pgavi",
            "id": "32k7rSC70F3C7qif9Pgavi",
            "name": "Humbreaders",
            "type": "artist",
            "uri": "spotify:artist:32k7rSC70F3C7qif9Pgavi"
          }
        ],
        "disc_number": 1,
        "track_number": 1,
        "duration_ms": 255980,
        "external_ids": {
          "isrc": "JPTF02418001"
        },
        "external_urls": {
          "spotify": "https://open.spotify.com/track/2l2JbsZwpWVsAMiScxTBfA"
        },
        "href": "https://api.spotify.com/v1/tracks/2l2JbsZwpWVsAMiScxTBfA",
        "id": "2l2JbsZwpWVsAMiScxTBfA",
        "name": "⚡️",
        "popularity": 43,
        "uri": "spotify:track:2l2JbsZwpWVsAMiScxTBfA",
        "is_local": false
      },
      "video_thumbnail": {
        "url": null
      }
    }
  ],
  "limit": 100,
  "next": null,
  "offset": 0,
  "previous": null,
  "total": 5
}
```
