# Generated by Django 4.2.6 on 2023-10-14 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('teamsize', models.IntegerField()),
                ('description', models.TextField()),
                ('image', models.CharField(blank=True, default='https://picsum.photos/200/300', max_length=100, null=True)),
                ('location', models.CharField(default='IIT Kharagpur', max_length=100)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
