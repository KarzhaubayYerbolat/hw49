from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('tasks/detail/<int:task_id>', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/new/', TaskCreateView.as_view(), name='create_task'),
    path('tasks/edit/<int:task_id>', TaskUpdateView.as_view(), name='edit_task'),
]
