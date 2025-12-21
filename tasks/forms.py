from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .validators import validate_username, validate_only_letters

Worker = get_user_model()


class WorkerCreationForm(UserCreationForm):
    first_name = forms.CharField(validators=[validate_only_letters], required=True)
    last_name = forms.CharField(validators=[validate_only_letters], required=True)

    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position")
        help_texts = {"username": ""}

    def clean_username(self):
        validate_username(self.cleaned_data.get("username"))
        return self.cleaned_data.get("username")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        validate_password(password, self.instance)
        return password


class WorkerChangeForm(UserChangeForm):
    password = None
    first_name = forms.CharField(validators=[validate_only_letters], required=True)
    last_name = forms.CharField(validators=[validate_only_letters], required=True)

    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position")
        help_texts = {"username": ""}

    def clean_username(self):
        validate_username(self.cleaned_data.get("username"))
        return self.cleaned_data.get("username")
