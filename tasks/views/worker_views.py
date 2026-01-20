from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Worker

class WorkerListView(LoginRequiredMixin, ListView):
    model = Worker
    template_name = "workers/worker_list.html"
    context_object_name = "workers"

    def get_queryset(self):
        return Worker.objects.select_related("position")

class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "workers/worker_detail.html"
    context_object_name = "worker"

    def get_queryset(self):
        return Worker.objects.select_related("position")
