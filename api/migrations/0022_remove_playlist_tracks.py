# Generated by Django 5.1.1 on 2024-10-12 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_library_albums_library_artists_library_playlists_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="playlist",
            name="tracks",
        ),
    ]
