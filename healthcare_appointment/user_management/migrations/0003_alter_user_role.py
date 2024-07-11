# Generated by Django 5.0.7 on 2024-07-11 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role_management', '0001_initial'),
        ('user_management', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, default='patient', null=True, on_delete=django.db.models.deletion.CASCADE, to='role_management.role'),
        ),
    ]
