# Spotify Dashboard

DashSpot is a dynamic visualizing dashboard designed to explore and analyze
Spotify libraries meant to be like an itunes style library browser.

It is built with Django, Postgres, Celery, and React on top of the Spotify API.

By adding additional integration with Wikipedia and MusicBrainz, DashSpot builds
a comprehensive database of music metadata relevant to them.

![DashSpot Screenshot](./doc/static/img/screencap.png)

Check out the [docs](https://dashspot-dev.netlify.app/)!

## Setup

Copy the sample `.env` file and fill in the necessary environment variables. I
use bitwarden to manage my secrets.

```bash
cp .env.sample .env
```

## Back-end

This is a Django application that uses REST framework for serializing and
deserializing objects.

## Front-end

This dashboard is built using React & Tailwind.

## Documentation

### Design

#### Colors

The colors are inspired by the Spotify brand colors and come from the base
colors in the Tailwind CSS framework.

Primary: Emerald 600
Secondary: Sky 500
Text: Zinc 800
Background: Neutral 200

## Spotify API

The core integration is built with Spotify.

### Attribution

From the [top tracks](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-users-top-artists-and-tracks) endpoint documentation:

> Please keep in mind that metadata, cover art and artist images must be
> accompanied by a link back to the applicable artist, album, track, or playlist
> on the Spotify Service.
>
> You must also attribute content from Spotify with the logo.
