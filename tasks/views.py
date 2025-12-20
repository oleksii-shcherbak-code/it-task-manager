from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import WorkerCreationForm, WorkerChangeForm
from .models import Task, Worker


def index(request):
    """Home Page"""
    context = {"title": "Home"}
    return render(request, "tasks/index.html", context=context)


class RegisterView(CreateView):
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class ProfileView(TemplateView):
    template_name = "profile.html"


class ProfileUpdateView(UpdateView):
    form_class = WorkerChangeForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "priority", "deadline", "task_type", "assignee"]
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse_lazy("task-list")


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "priority", "deadline", "task_type", "assignee", "is_completed"]
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse_lazy("task-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")


class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "workers/worker_list.html"
    context_object_name = "workers"


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "workers/worker_detail.html"
    context_object_name = "worker"
