# Generated by Django 4.2.13 on 2024-09-04 11:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_alter_likes_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="subcategory",
            name="is_payment",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="price",
            field=models.BigIntegerField(default=0),
        ),
    ]
