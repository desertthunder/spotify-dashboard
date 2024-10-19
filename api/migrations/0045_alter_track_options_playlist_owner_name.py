# Generated by Django 5.1.1 on 2024-10-19 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0044_alter_library_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="track",
            options={
                "ordering": ["-is_analyzed", "-is_synced", "-created_at", "-updated_at"]
            },
        ),
        migrations.AddField(
            model_name="playlist",
            name="owner_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]