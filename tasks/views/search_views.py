from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from rapidfuzz import fuzz
from tasks.models import Task, Worker


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        context["query"] = query
        if not query:
            context["workers"] = []
            context["tasks"] = []
            return context
        workers_qs = (
            Worker.objects.select_related("position")
            .only("id", "first_name", "last_name", "position__name")
            .filter(first_name__icontains=query)
            | Worker.objects.select_related("position")
            .only("id", "first_name", "last_name", "position__name")
            .filter(last_name__icontains=query)
        ).distinct()
        workers = []
        for worker in workers_qs:
            full_name = f"{worker.first_name} {worker.last_name}"
            score = fuzz.partial_ratio(query.lower(), full_name.lower())
            if score > 60:
                workers.append(worker)
        tasks_qs = (
            Task.objects.select_related("assignee", "task_type")
            .only("id", "title", "assignee__username", "task_type__name")
            .filter(title__icontains=query)
        )
        tasks = []
        for task in tasks_qs:
            score = fuzz.partial_ratio(query.lower(), task.title.lower())
            if score > 60:
                tasks.append(task)
        context["workers"] = workers
        context["tasks"] = tasks
        return context

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
            suggestions.append({"type": "worker", "name": full_name, "id": worker.id})
    for task in Task.objects.all():
        if query.lower() in task.title.lower():
            suggestions.append({"type": "task", "name": task.title, "id": task.id})
    return JsonResponse(suggestions[:5], safe=False)
