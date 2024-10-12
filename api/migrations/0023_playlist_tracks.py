# Generated by Django 5.1.1 on 2024-10-12 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0022_remove_playlist_tracks"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlist",
            name="tracks",
            field=models.ManyToManyField(related_name="playlists", to="api.track"),
        ),
    ]
