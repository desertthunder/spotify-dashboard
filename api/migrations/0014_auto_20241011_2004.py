"""Generated by Django 5.1.1 on 2024-10-11 20:04."""

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0013_rename_user_id_playlist_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="album",
            name="identity",
            field=models.UUIDField(default=uuid.uuid4, unique=True, null=True),
        ),
        migrations.AddField(
            model_name="artist",
            name="identity",
            field=models.UUIDField(default=uuid.uuid4, unique=True, null=True),
        ),
        migrations.AddField(
            model_name="playlist",
            name="identity",
            field=models.UUIDField(default=uuid.uuid4, unique=True, null=True),
        ),
        migrations.AddField(
            model_name="track",
            name="identity",
            field=models.UUIDField(default=uuid.uuid4, unique=True, null=True),
        ),
    ]
