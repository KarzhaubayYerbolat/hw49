# Generated by Django 5.0.1 on 2024-01-26 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20240126_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_type_old',
        ),
    ]