from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rapidfuzz import fuzz

from .forms import WorkerCreationForm, WorkerChangeForm
from .models import Task, Worker, TaskType, AVATAR_CHOICES


# -----------------------------
# Home (Login Required)
# -----------------------------
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Home"
        context["tasks_total"] = Task.objects.count()
        context["tasks_active"] = Task.objects.filter(is_completed=False).count()
        context["tasks_completed"] = Task.objects.filter(is_completed=True).count()
        context["workers_total"] = Worker.objects.count()

        return context


# -----------------------------
# Auth & Profile
# -----------------------------
class RegisterView(CreateView):
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = WorkerChangeForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user


# -----------------------------
# Workers
# -----------------------------
class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "workers/worker_list.html"
    context_object_name = "workers"


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "workers/worker_detail.html"
    context_object_name = "worker"


# -----------------------------
# Tasks
# -----------------------------
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        sort = self.request.GET.get("sort")
        direction = self.request.GET.get("dir", "asc")

        if sort in ["title", "deadline", "priority", "is_completed"]:
            if direction == "desc":
                return qs.order_by(f"-{sort}")
            return qs.order_by(sort)

        if sort == "assignee":
            if direction == "desc":
                return qs.order_by("-assignee__username")
            return qs.order_by("assignee__username")

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["current_sort"] = self.request.GET.get("sort", "")
        ctx["current_dir"] = self.request.GET.get("dir", "asc")
        return ctx


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


# -----------------------------
# Task Types (Login Required)
# -----------------------------
class TaskTypeListView(LoginRequiredMixin, ListView):
    model = TaskType
    template_name = "task_type/task_type_list.html"
    context_object_name = "task_types"


class TaskTypeDetailView(LoginRequiredMixin, DetailView):
    model = TaskType
    template_name = "task_type/task_type_detail.html"
    context_object_name = "task_type"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(task_type=self.object)
        return context


class TaskTypeCreateView(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = ["name"]
    template_name = "task_type/task_type_form.html"
    success_url = reverse_lazy("task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = ["name"]
    template_name = "task_type/task_type_form.html"
    success_url = reverse_lazy("task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskType
    template_name = "task_type/task_type_confirm_delete.html"
    success_url = reverse_lazy("task-type-list")


@login_required
def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)

    task.is_completed = not task.is_completed
    task.save()

    return redirect("task-detail", pk=pk)


class TaskTypeAnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = "task_type/task_type_analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_month = timezone.now() - timedelta(days=30)

        context["tasks_by_type"] = (
            Task.objects.filter(created_at__gte=last_month)
            .values("task_type__name")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        context["completed_by_type"] = (
            Task.objects.filter(is_completed=True, updated_at__gte=last_month)
            .values("task_type__name")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        return context


# -----------------------------
# Search (Fuzzy Search)
# -----------------------------
class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "").strip()
        context["query"] = query

        if not query:
            context["tasks"] = []
            context["workers"] = []
            return context

        workers = []
        for worker in Worker.objects.all():
            full_name = f"{worker.first_name} {worker.last_name}"
            score = fuzz.partial_ratio(query.lower(), full_name.lower())
            if score > 60:
                workers.append(worker)

        tasks = []
        for task in Task.objects.all():
            score = fuzz.partial_ratio(query.lower(), task.title.lower())
            if score > 60:
                tasks.append(task)

        context["workers"] = workers
        context["tasks"] = tasks

        return context


# -----------------------------
# Autocomplete Suggestions (Login Required)
# -----------------------------
def search_suggest(request):
    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)

    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse([], safe=False)

    suggestions = []

    for worker in Worker.objects.all():
        full_name = f"{worker.first_name} {worker.last_name}"
        if query.lower() in full_name.lower():
            suggestions.append({
                "type": "worker",
                "name": full_name,
                "id": worker.id,
            })

    for task in Task.objects.all():
        if query.lower() in task.title.lower():
            suggestions.append({
                "type": "task",
                "name": task.title,
                "id": task.id,
            })

    return JsonResponse(suggestions[:5], safe=False)


# -----------------------------
# Avatar Change
# -----------------------------
class AvatarChangeView(LoginRequiredMixin, TemplateView):
    template_name = "avatar_change.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatars"] = [choice[0] for choice in AVATAR_CHOICES]
        return context

    def post(self, request, *args, **kwargs):
        avatar = request.POST.get("avatar")

        if avatar:
            request.user.avatar = avatar
            request.user.save()

        return self.get(request, *args, **kwargs)
