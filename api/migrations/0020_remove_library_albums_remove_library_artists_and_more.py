# Generated by Django 5.1.1 on 2024-10-12 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0019_playlist_is_analyzed_playlist_is_synced"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="library",
            name="albums",
        ),
        migrations.RemoveField(
            model_name="library",
            name="artists",
        ),
        migrations.RemoveField(
            model_name="library",
            name="playlists",
        ),
        migrations.RemoveField(
            model_name="library",
            name="tracks",
        ),
    ]