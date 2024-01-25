from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_required(TaskListView.as_view()), name='task_list'),
    path('tasks/detail/<int:task_id>', login_required(TaskDetailView.as_view()), name='task_detail'),
    path('tasks/new/', login_required(TaskCreateView.as_view()), name='create_task'),
    path('tasks/edit/<int:task_id>', login_required(TaskUpdateView.as_view()), name='edit_task'),
    path('tasks/delete/<int:task_id>', login_required(TaskDeleteView.as_view()), name='delete_task'),
    path('tasks/take/<int:task_id>', login_required(TaskTakeView.as_view()), name='take_task'),
    path('tasks/reject/<int:task_id>', login_required(RejectTaskView.as_view()), name='reject_task'),
    path('tasks/solve/<int:task_id>', login_required(TaskSolveView.as_view()), name='solve_task'),
    path('tasks/setexecutor/<int:task_id>', login_required(ChangeTaskExecutorView.as_view()), name='set_executor'),
]

# Test user: login: admin, password: 123
