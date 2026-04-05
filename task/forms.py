from django import forms 
from .models import Task,Categories

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['user']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        exclude = ['user']