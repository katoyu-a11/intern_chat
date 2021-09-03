from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ImageModel, TalkModel
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'


class TalkForm(forms.ModelForm):
    class Meta:
        model = TalkModel
        fields = ['content']

class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class MailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class PasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    



