# Generated by Django 4.2.6 on 2023-10-12 18:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0007_alter_competition_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 12, 18, 29, 50, 405236, tzinfo=datetime.timezone.utc)),
        ),
    ]
