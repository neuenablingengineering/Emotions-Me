from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'account_type')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = UserChangeForm.Meta.fields
