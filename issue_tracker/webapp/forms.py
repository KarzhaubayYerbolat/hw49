from django import forms
from django.core.exceptions import ValidationError

from .models import Task, TaskType, Solution
from appuser.models import Team, AppUser


class TaskCreateOrUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'task_types',
            'responsible_group',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    task_types = forms.ModelMultipleChoiceField(
        queryset=TaskType.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    responsible_group = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )


class TaskSolutionForm(forms.ModelForm):

    class Meta:
        model = Solution
        fields = ['solution_description',]
        widgets = {
            'solution_description': forms.Textarea(attrs={
                'class': 'form-control d-flex',
                'placeholder': 'Write solution',
                'rows': 7,
            }),
        }


def create_executor_change_form(team):
    class TaskExecutorForm(forms.Form):
        executor = forms.ModelChoiceField(
            queryset=AppUser.objects.filter(team=team),
            widget=forms.Select(attrs={'class': 'form-control'},)

        )
    return TaskExecutorForm
