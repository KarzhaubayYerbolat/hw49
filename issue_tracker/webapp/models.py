from django.db import models
from .model_utils import ReturnTitleStrMixin
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Task(ReturnTitleStrMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Create datetime')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Last update')
    complete_datetime = models.DateTimeField(verbose_name='Complete datetime', null=True, blank=True)
    status = models.ForeignKey(
        'webapp.Status',
        on_delete=models.PROTECT,
        verbose_name='Status',
        related_name='tasks_with_status',

    )
    task_type = models.ForeignKey(
        'webapp.TaskType',
        on_delete=models.PROTECT,
        verbose_name='Type',
        related_name='tasks_with_type',
    )
    initiator = models.ForeignKey(
        'appuser.AppUser',
        on_delete=models.PROTECT,
        verbose_name='Initiator',
        related_name='tasks_initiated',
    )
    responsible_group = models.ForeignKey(
        'appuser.Team',
        on_delete=models.PROTECT,
        verbose_name='Responsible Group',
        related_name='tasks_with_responsible_group'
    )
    executor = models.ForeignKey(
        'appuser.AppUser',
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Executor',
        related_name='tasks_executed',
        blank=True
    )


class Solution(models.Model):
    task = models.OneToOneField(
        'webapp.Task',
        on_delete=models.CASCADE,
        verbose_name='Linked Task',
        related_name='solution',
        null=True,
    )
    solution_description = models.TextField(
        verbose_name='Solution',
        validators=[MaxLengthValidator(200), MinLengthValidator(20)]
    )

    def __str__(self):
        return self.solution_description[:20]


class Status(ReturnTitleStrMixin, models.Model):
    title = models.CharField(max_length=30, verbose_name='Status')


class TaskType(ReturnTitleStrMixin, models.Model):
    title = models.CharField(max_length=30, verbose_name='Type')
