from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from webapp.forms import TaskCreateOrUpdateForm
from webapp.models import Task


class TaskFormMixin:
    template = 'webapp/create_or_update_task.html'
    action = None
    form = TaskCreateOrUpdateForm
    model = Task

    def get(self, request, **kwargs):
        context = self.get_custom_context(**kwargs)
        return render(request, self.template, context)

    def get_custom_context(self, **kwargs):
        context = kwargs
        context['action'] = self.action
        if self.action == 'Create':
            context['form_action'] = '/tasks/new/'
            context['form'] = self.form()
        if self.action == 'Update':
            context['form_action'] = f'/tasks/edit/{kwargs['task_id']}'
            task = get_object_or_404(self.model, id=kwargs['task_id'])
            context['form'] = self.form(instance=task)
        return context


class CanEditTaskCheckMixin:
    action = None
    error_messages = {
        'Update': 'Only the initiator or superuser can edit this task and task status should be New',
        'Delete': 'Only the initiator or superuser can delete this task',
        'Take': ('You cannot take this task for the following possible reasons:\n'
                 '1)This task already has an executor;\n'
                 '2)You are not a member of the responsible team for this assignment;\n'
                 '3)This task has been rejected;\n'),
        'Reject': ('You cannot reject this assignment for the following reasons:\n'
                   '1)You are not the team leader of the group responsible for this task;\n'
                   '2)The task is already rejected;\n'),
        'Solve': ('You cannot solve this task for the following reasons:\n'
                  '1)You are not a executor of this task\n'),
        'ChangeExecutor': 'Only team leader can change executor'
    }

    def check_permissions(self, request, task):
        if self.action =='Update' and task.initiator == request.user and task.status.title == 'New':
            return True

        elif self.action == 'Delete' and request.user == task.initiator or request.user.is_superuser:
            return True

        elif (self.action == 'Take' and
              request.user.team == task.responsible_group and
              task.executor is None and
              task.status.title != 'Rejected'):
            return True

        elif (self.action == 'Reject' and
              task.responsible_group.team_lead == request.user and
              task.status.title != 'Rejected'):
            return True

        elif self.action == 'Solve' and request.user == task.executor and task.status != 'Rejected':
            return True

        elif self.action == 'ChangeExecutor' and request.user == task.responsible_group.team_lead:
            return True

        error = self.error_messages.get(self.action, 'Invalid action')
        messages.add_message(request, messages.ERROR, error)
        return redirect(reverse('task_detail', kwargs={'task_id': task.id}))
