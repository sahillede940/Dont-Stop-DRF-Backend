# Generated by Django 4.2.6 on 2023-10-11 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='image',
            field=models.CharField(blank=True, default='https://picsum.photos/200/300', max_length=100, null=True),
        ),
    ]
