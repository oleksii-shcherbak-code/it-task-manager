from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from tasks.models import TaskType, Task


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
        context["tasks"] = Task.objects.filter(task_type=self.object).select_related("assignee", "task_type")
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
