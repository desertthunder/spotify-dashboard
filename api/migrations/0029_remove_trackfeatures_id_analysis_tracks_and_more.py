# Generated by Django 5.1.1 on 2024-10-12 03:29

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0028_remove_analysis_playlist_remove_analysis_tracks_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trackfeatures",
            name="id",
        ),
        migrations.AddField(
            model_name="analysis",
            name="tracks",
            field=models.ManyToManyField(related_name="analyses", to="api.track"),
        ),
        migrations.AddField(
            model_name="analysis",
            name="user",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="trackfeatures",
            name="identity",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="trackfeatures",
            name="track",
            field=models.OneToOneField(
                default=uuid.uuid4,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="features",
                to="api.track",
            ),
            preserve_default=False,
        ),
    ]
