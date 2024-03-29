# Generated by Django 5.0.1 on 2024-01-26 05:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_alter_task_complete_datetime_alter_task_executor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_type',
            new_name='task_type_old',
        ),
        migrations.AlterField(
            model_name='solution',
            name='solution_description',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(200), django.core.validators.MinLengthValidator(20)], verbose_name='Solution'),
        ),
    ]
