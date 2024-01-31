from django import forms
from django.forms import ValidationError
import enchant
from .models import Task, TaskType, Solution
from appuser.models import Team, AppUser


def is_symbol(string):
    symbols = '~`!@#$%^&*()-+/?><:;"|]}[{'
    if string in symbols:
        return True
    else:
        return False


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

    def clean_title(self):
        en_us_dict = enchant.Dict("en_US")
        title = self.cleaned_data.get('title')

        for elm in title.split():
            if is_symbol(elm) or elm.isdigit():
                continue

            if not en_us_dict.check(elm):
                raise ValidationError('Only english words!')

        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 15:
            raise ValidationError("Min length must be greater than 15!")
        return description


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
