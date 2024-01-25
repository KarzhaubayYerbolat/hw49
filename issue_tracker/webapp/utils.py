from django.shortcuts import get_object_or_404, render

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
