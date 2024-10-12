# Generated by Django 5.1.1 on 2024-10-12 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_remove_library_albums_remove_library_artists_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="library",
            name="albums",
            field=models.ManyToManyField(related_name="libraries", to="api.album"),
        ),
        migrations.AddField(
            model_name="library",
            name="artists",
            field=models.ManyToManyField(related_name="libraries", to="api.artist"),
        ),
        migrations.AddField(
            model_name="library",
            name="playlists",
            field=models.ManyToManyField(related_name="libraries", to="api.playlist"),
        ),
        migrations.AddField(
            model_name="library",
            name="tracks",
            field=models.ManyToManyField(related_name="libraries", to="api.track"),
        ),
    ]