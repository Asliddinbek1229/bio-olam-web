# Generated by Django 5.0 on 2024-05-30 08:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0007_subcategory_descriptions"),
        ("users", "0006_profile_saved_playlists"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="saved_playlists",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="saved_by_users",
                to="courses.subcategory",
            ),
        ),
    ]