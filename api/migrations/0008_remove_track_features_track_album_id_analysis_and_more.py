# Generated by Django 5.1.1 on 2024-10-10 05:17

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_album_created_at_album_updated_at_artist_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="track",
            name="features",
        ),
        migrations.AddField(
            model_name="track",
            name="album_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tracks",
                to="api.album",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Analysis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "public_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("version", models.CharField(max_length=255, unique=True)),
                (
                    "playlist_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="analysis",
                        to="api.playlist",
                    ),
                ),
                (
                    "tracks",
                    models.ManyToManyField(related_name="analyses", to="api.track"),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TrackFeatures",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "public_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("danceability", models.FloatField()),
                ("energy", models.FloatField()),
                ("key", models.IntegerField()),
                ("loudness", models.FloatField()),
                ("mode", models.IntegerField()),
                ("speechiness", models.FloatField()),
                ("acousticness", models.FloatField()),
                ("instrumentalness", models.FloatField()),
                ("liveness", models.FloatField()),
                ("valence", models.FloatField()),
                ("tempo", models.FloatField()),
                ("duration_ms", models.IntegerField()),
                ("time_signature", models.IntegerField()),
                (
                    "track",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="features",
                        to="api.track",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
