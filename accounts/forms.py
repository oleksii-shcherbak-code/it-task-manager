from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .validators import validate_username, validate_only_letters

Worker = get_user_model()


class OnlyLettersCharField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("validators", [validate_only_letters])
        super().__init__(*args, **kwargs)


class BaseWorkerForm(forms.ModelForm):
    first_name = OnlyLettersCharField(required=True)
    last_name = OnlyLettersCharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position")
        help_texts = {"username": None}

    def clean_username(self):
        validate_username(self.cleaned_data.get("username"))
        return self.cleaned_data.get("username")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Worker.objects.filter(email=email).exists():
            raise forms.ValidationError("Email must be unique.")
        return email


class WorkerCreationForm(BaseWorkerForm, UserCreationForm):
    class Meta(BaseWorkerForm.Meta, UserCreationForm.Meta):
        pass


class WorkerChangeForm(BaseWorkerForm, UserChangeForm):
    password = None

    class Meta(BaseWorkerForm.Meta, UserChangeForm.Meta):
        pass
