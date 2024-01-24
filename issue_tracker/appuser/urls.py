from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LoginUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(redirect_authenticated_user=True), name='loginuser'),
    path('logout/', LogoutView.as_view(next_page='task_list'), name='logout'),
]