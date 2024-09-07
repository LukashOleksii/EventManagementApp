# Generated by Django 4.2.16 on 2024-09-06 15:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_remove_event_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
    ]
