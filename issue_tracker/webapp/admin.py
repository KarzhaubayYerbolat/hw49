from django.contrib import admin
from .models import *


class TaskSolutionInline(admin.StackedInline):
    model = Solution


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'types', 'status', 'initiator', 'responsible_group', 'executor')
    inlines = (TaskSolutionInline,)

    def types(self, obj):
        types_str = ', '.join([task_type.title for task_type in obj.task_types.all()])
        return types_str


admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(TaskType)
