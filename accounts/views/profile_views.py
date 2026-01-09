from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from accounts.forms import WorkerChangeForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = WorkerChangeForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user
