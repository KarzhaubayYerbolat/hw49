from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_required(TaskListView.as_view()), name='task_list'),
    path('tasks/detail/<int:task_id>', login_required(TaskDetailView.as_view()), name='task_detail'),
    path('tasks/new/', login_required(TaskCreateView.as_view()), name='create_task'),
    path('tasks/edit/<int:task_id>', login_required(TaskUpdateView.as_view()), name='edit_task'),
]

# Test user: login: admin, password: 123
