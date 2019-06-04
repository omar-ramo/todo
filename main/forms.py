from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'do_before')

    def clean_do_before(self):
        do_before_date = self.cleaned_data.get('do_before')
        if do_before_date < timezone.now():
            raise forms.ValidationError(
                '"do before" date can not be in the past'
            )
        return do_before_date
