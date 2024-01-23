from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
]
