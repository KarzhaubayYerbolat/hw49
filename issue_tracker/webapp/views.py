from django.views.generic import TemplateView
from .models import Task


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
        return queryset
