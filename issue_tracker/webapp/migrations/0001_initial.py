# Generated by Django 5.0.1 on 2024-01-23 05:10

import django.db.models.deletion
import webapp.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution_description', models.TextField(verbose_name='Solution')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Status')),
            ],
            bases=(webapp.utils.ReturnTitleStrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Type')),
            ],
            bases=(webapp.utils.ReturnTitleStrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Create datetime')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Last update')),
                ('complete_datetime', models.DateTimeField(verbose_name='Complete datetime')),
                ('executor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tasks_executed', to=settings.AUTH_USER_MODEL, verbose_name='Executor')),
                ('initiator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_initiated', to=settings.AUTH_USER_MODEL, verbose_name='Initiator')),
                ('responsible_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_with_responsible_group', to='auth.group', verbose_name='Responsible Group')),
                ('solution', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task', to='webapp.solution', verbose_name='Task Solution')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_with_status', to='webapp.status', verbose_name='Status')),
                ('task_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_with_type', to='webapp.tasktype', verbose_name='Type')),
            ],
            bases=(webapp.utils.ReturnTitleStrMixin, models.Model),
        ),
    ]