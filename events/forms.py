from django import forms
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'location', 'members']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        instance = kwargs.get('instance')
        
        if instance:
            initial = kwargs.setdefault('initial', {})
            
            if instance.date:
                initial['date'] = instance.date.date()
                initial['time'] = instance.date.time()

        super().__init__(*args, **kwargs)

        if current_user:
            self.fields['members'].queryset = User.objects.exclude(id=current_user.id)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            cleaned_data['datetime'] = datetime.combine(date, time)
        else:
            cleaned_data['datetime'] = None

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.date = self.cleaned_data['datetime']
        
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
