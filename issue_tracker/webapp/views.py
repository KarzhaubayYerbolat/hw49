from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from .models import Task, Status
from .forms import TaskCreateOrUpdateForm
from .utils import TaskFormMixin


class TaskListView(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.get_queryset()
        context['page_title'] = 'Task List'
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        team_filter = self.request.GET.get('team', None)
        executor_filter = self.request.GET.get('executor', None)
        initiator_filter = self.request.GET.get('initiator', None)
        if team_filter:
            queryset = Task.objects.filter(responsible_group__title=team_filter)
        if executor_filter:
            queryset = Task.objects.filter(executor__username=executor_filter)
        if initiator_filter:
            queryset = Task.objects.filter(initiator__username=initiator_filter)
        return queryset.order_by('-create_datetime')


class TaskDetailView(TemplateView):
    template_name = 'webapp/task_detail.html'

    def get_context_data(self, task_id, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(id=task_id)
        context['task'] = task
        context['page_title'] = f'Task-{task_id} {task.title}'
        return context


class TaskCreateView(TaskFormMixin, View):
    action = 'Create'

    def post(self, request):
        form = TaskCreateOrUpdateForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.initiator = self.request.user
            obj.status = Status.objects.get(title='New')
            obj.save()
            return redirect(reverse('task_detail', kwargs={'task_id': obj.id}))

        else:
            context = self.get_custom_context()
            context['form'] = form
            return render(request, self.template, context)


class TaskUpdateView(TaskFormMixin, View):
    action = 'Update'

    def post(self, request, task_id):
        task = get_object_or_404(self.model, id=task_id)
        form = TaskCreateOrUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('task_detail', kwargs={'task_id': task.id}))

        else:
            context = self.get_custom_context()
            context['form'] = form
            return render(request, self.template, context)


class TaskDeleteView(View):

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if request.user == task.initiator or request.user.is_superuser:
            task.delete()
            return redirect('task_list')
        else:
            messages.add_message(request, messages.ERROR, "Only the initiator or superuser can delete this task")
            return redirect(reverse('task_detail', kwargs={'task_id': task_id}))

