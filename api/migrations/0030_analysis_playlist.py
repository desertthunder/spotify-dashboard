# Generated by Django 5.1.1 on 2024-10-12 03:30

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0029_remove_trackfeatures_id_analysis_tracks_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="analysis",
            name="playlist",
            field=models.OneToOneField(
                default=uuid.uuid4,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analysis",
                to="api.playlist",
            ),
            preserve_default=False,
        ),
    ]
