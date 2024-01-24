from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginUserForm


class LoginUserView(LoginView):
    template_name = 'appuser/login_user.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'Login'
        return context
