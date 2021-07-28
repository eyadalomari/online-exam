from django import forms
from django.contrib.auth.models import User
from .models import Question

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form_input'}))
    email = forms.EmailField(required=True, widget = forms.TextInput(attrs={'class': 'form_input'}))
    class Meta():
        model = User
        fields = ('username','email', 'password')
        help_texts = {
            'username': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_input'}),
        }


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form_input'}))
    class Meta():
        model = User
        fields = ('username', 'password')
        help_texts = {
            'username': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_input'}),
        }


class QuestionForm(forms.ModelForm):
    question = forms.CharField(label='')
    A = forms.CharField(widget=forms.RadioSelect, label='A')
    B = forms.CharField(widget=forms.RadioSelect, label='B')
    C = forms.CharField(widget=forms.RadioSelect, label='C')
    D = forms.CharField(widget=forms.RadioSelect, label='D')
    class Meta():
        model = Question
        fields = ('question','A', 'B', 'C', 'D')
        help_texts = {
            'username': None,
        }
