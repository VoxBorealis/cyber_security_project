from pyexpat import model
from attr import fields
from django import forms
from .models import User, Task

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username", "password")

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_text', 'owner')

class SearchForm(forms.Form):
    query = forms.CharField(label="", max_length=200)
