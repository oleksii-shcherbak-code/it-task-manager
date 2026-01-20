from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Case, When, IntegerField
from tasks.models import Task, Worker


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks_stats = Task.objects.aggregate(
            total=Count("id"),
            active=Count(Case(When(is_completed=False, then=1), output_field=IntegerField())),
            completed=Count(Case(When(is_completed=True, then=1), output_field=IntegerField())),
        )
        context.update({
            "title": "Home",
            "tasks_total": tasks_stats["total"],
            "tasks_active": tasks_stats["active"],
            "tasks_completed": tasks_stats["completed"],
            "workers_total": Worker.objects.count(),
        })
        return context
