# Generated by Django 5.0 on 2024-05-30 11:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0009_remove_videos_comments_count_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="videos",
            name="created_at",
        ),
    ]