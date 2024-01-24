from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from .models import Task, Status
from .forms import TaskCreateForm


class TaskListView(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):

        context = super(TaskListView, self).get_context_data(**kwargs)
        context['tasks'] = self.get_queryset()
        context['page_title'] = 'Task List'
        return context

    def get_queryset(self):
        model = Task
        queryset = model.objects.all()
        team_filter = self.request.GET.get('team', None)
        executor_filter = self.request.GET.get('executor', None)
        initiator_filter = self.request.GET.get('initiator', None)
        if team_filter:
            queryset = model.objects.filter(responsible_group__title=team_filter)
        if executor_filter:
            queryset = model.objects.filter(executor__username=executor_filter)
        if initiator_filter:
            queryset = model.objects.filter(initiator__username=initiator_filter)
        return queryset.order_by('-create_datetime')


class TaskDetailView(TemplateView):
    template_name = 'webapp/task_detail.html'

    def get_context_data(self, task_id, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        task = Task.objects.get(id=task_id)
        context['task'] = task
        context['page_title'] = f'Task-{task_id} {task.title}'
        return context


class TaskCreateView(View):
    template = 'webapp/create_task.html'

    def get(self, request):
        form = TaskCreateForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = TaskCreateForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.initiator = self.request.user
            obj.status = Status.objects.get(title='New')
            obj.save()
            return redirect(reverse('task_detail', kwargs={'task_id': obj.id}))

        else:
            context = {'form': form}
            return render(request, self.template, context)
