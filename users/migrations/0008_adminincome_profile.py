# Generated by Django 4.2.13 on 2024-10-03 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_adminincome_delete_adminearnings_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="adminincome",
            name="profile",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
    ]
