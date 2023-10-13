# Generated by Django 4.2.6 on 2023-10-11 16:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0004_alter_competition_applied_users_and_more'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.CreateModel(
            name='UserSelector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True, null=True)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_competition', to='competition.competition')),
                ('user_applied', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_competition_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]