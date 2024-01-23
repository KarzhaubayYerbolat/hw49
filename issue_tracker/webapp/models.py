from django.db import models


class ReturnStrMixin:
    title = None

    def __str__(self):
        return self.title


class Task(ReturnStrMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Create date')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Last update')


class Status(ReturnStrMixin, models.Model):
    title = models.CharField(max_length=30, verbose_name='Status')


class TaskType(ReturnStrMixin, models.Model):
    title = models.CharField(max_length=30, verbose_name='Type')

