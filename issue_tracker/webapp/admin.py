from django.contrib import admin
from .models import *


class TaskSolutionInline(admin.StackedInline):
    model = Solution


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'types', 'status', 'initiator', 'responsible_group', 'executor')
    inlines = (TaskSolutionInline,)


admin.site.register(Task, TaskAdmin)
admin.site.register(Status)
admin.site.register(TaskType)
