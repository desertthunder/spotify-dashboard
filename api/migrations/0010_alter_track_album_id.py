# Generated by Django 5.1.1 on 2024-10-10 05:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_alter_playlist_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="track",
            name="album_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tracks",
                to="api.album",
            ),
        ),
    ]
