# Generated by Django 5.0.7 on 2024-07-12 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='deleted_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]