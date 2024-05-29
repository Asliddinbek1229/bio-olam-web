from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime.now),
            preserve_default=False,
        ),
    ]
