from django import forms
from django.core.exceptions import ValidationError

from .models import Task, TaskType
from appuser.models import Team


class TaskCreateOrUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'task_type',
            'responsible_group',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    responsible_group = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

