import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from .models import Task, Status
from .forms import TaskCreateOrUpdateForm, TaskSolutionForm, create_executor_change_form
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
        if task.executor == self.request.user:
            context['form_solve'] = TaskSolutionForm()

        if task.responsible_group.team_lead == self.request.user and task.status.title != 'Rejected':

            context['form_executor'] = create_executor_change_form(task.responsible_group)(data={
                'executor': task.executor
            })
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
        if task.initiator == request.user and task.status.title == 'New':
            form = TaskCreateOrUpdateForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect(reverse('task_detail', kwargs={'task_id': task.id}))

            else:
                context = self.get_custom_context()
                context['form'] = form
                return render(request, self.template, context)
        else:
            message = 'Only the initiator or superuser can edit this task and task status should be New'
            messages.add_message(request, messages.ERROR, message)
            return redirect(reverse('task_detail', kwargs={'task_id': task_id}))


class TaskDeleteView(View):

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if request.user == task.initiator or request.user.is_superuser:
            task.delete()
            return redirect('task_list')
        else:
            message = 'Only the initiator or superuser can delete this task'
            messages.add_message(request, messages.ERROR, message)
            return redirect(reverse('task_detail', kwargs={'task_id': task_id}))


class TaskTakeView(View):

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if request.user.team == task.responsible_group and task.executor is None and task.status.title != 'Rejected':
            task.status = Status.objects.get(title='In Progress')
            task.executor = request.user
            task.save()

        else:
            message = ('You cannot take this task for the following possible reasons:\n'
                       '1)This task already has an executor;\n'
                       '2)You are not a member of the responsible team for this assignment;\n'
                       '3)This task has been rejected;\n')
            messages.add_message(request, messages.ERROR, message)

        return redirect(reverse('task_detail', kwargs={'task_id': task_id}))


class RejectTaskView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if task.responsible_group.team_lead == request.user and task.status.title != 'Rejected':
            task.status = Status.objects.get(title='Rejected')
            task.executor = None
            task.save()

        else:
            message = ('You cannot reject this assignment for the following reasons:\n'
                       '1)You are not the team leader of the group responsible for this task;\n'
                       '2)The task is already rejected;\n')
            messages.add_message(request, messages.ERROR, message)

        return redirect(reverse('task_detail', kwargs={'task_id': task_id}))


class TaskSolveView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if request.user == task.executor:
            form = TaskSolutionForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.task = task
                task.status = Status.objects.get(title='Done')
                task.complete_datetime = datetime.datetime.now()
                task.save()
                obj.save()

            else:
                messages.add_message(request, messages.ERROR, form.errors)
            return redirect(reverse('task_detail', kwargs={'task_id': task_id}))


class ChangeTaskExecutorView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        if request.user == task.responsible_group.team_lead:
            form = create_executor_change_form(request.user.team)(self.request.POST)
            if form.is_valid():
                task.executor = form.cleaned_data['executor']
                task.status = Status.objects.get(title='In Progress')
                task.save()

            else:
                messages.add_message(request, messages.ERROR, form.errors)
            return redirect(reverse('task_detail', kwargs={'task_id': task_id}))

        else:
            message = 'Only team leader of responsible group can change executor'
            messages.add_message(request, messages.ERROR, message)
