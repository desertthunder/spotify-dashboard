# Generated by Django 5.1.1 on 2024-10-14 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0041_remove_genre_albums_album_genres"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="genre",
            name="artists",
        ),
        migrations.AddField(
            model_name="artist",
            name="genres",
            field=models.ManyToManyField(related_name="artists", to="api.genre"),
        ),
    ]
