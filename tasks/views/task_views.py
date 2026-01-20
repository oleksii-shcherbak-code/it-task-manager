from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Case, When, IntegerField
from django.shortcuts import get_object_or_404, redirect
from tasks.models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("assignee", "task_type")
        sort = self.request.GET.get("sort")
        direction = self.request.GET.get("dir", "asc")
        desc = "-" if direction == "desc" else ""
        priority_order = Case(
            When(priority="low", then=1),
            When(priority="medium", then=2),
            When(priority="high", then=3),
            When(priority="urgent", then=4),
            output_field=IntegerField(),
        )
        qs = qs.annotate(priority_order=priority_order)
        if sort == "priority":
            return qs.order_by(f"{desc}priority_order")
        if sort in ["title", "deadline", "is_completed"]:
            return qs.order_by(f"{desc}{sort}")
        if sort == "assignee":
            return qs.order_by(f"{desc}assignee__username")
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

    def get_queryset(self):
        return Task.objects.select_related("assignee", "task_type")

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

def toggle_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_completed = not task.is_completed
    task.save()
    return redirect("task-detail", pk=pk)
