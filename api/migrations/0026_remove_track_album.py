# Generated by Django 5.1.1 on 2024-10-12 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0025_album_artists"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="track",
            name="album",
        ),
    ]
