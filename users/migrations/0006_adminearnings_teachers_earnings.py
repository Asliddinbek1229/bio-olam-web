# Generated by Django 4.2.13 on 2024-10-03 06:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_purchasedplaylist"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminEarnings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name="teachers",
            name="earnings",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
