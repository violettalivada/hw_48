from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class MyUserCreationForm(UserCreationForm):
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'validate', }))

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=commit)
        Profile.objects.create(user=user)
        return user
