import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

Worker = get_user_model()


def validate_username(username: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        raise forms.ValidationError(
            "Username may contain only Latin letters, digits, and the '_' symbol."
        )
    if username.count("_") > 1:
        raise forms.ValidationError(
            "Username may contain at most one '_' symbol."
        )
    if len(username) < 3 or len(username) > 30:
        raise forms.ValidationError(
            "Username must be between 3 and 30 characters long."
        )
    return username


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ("username", "email", "position")
        help_texts = {
            "username": ""  # 🔥 убираем help_text
        }

    def clean_username(self):
        return validate_username(self.cleaned_data.get("username"))


class WorkerChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = Worker
        fields = ("username", "email", "position")
        help_texts = {
            "username": ""
        }

    def clean_username(self):
        return validate_username(self.cleaned_data.get("username"))
