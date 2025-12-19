from django.contrib import admin
from .models import Task, TaskType


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "assignee", "task_type", "priority", "deadline", "is_completed")
    list_filter = ("priority", "is_completed", "task_type")
    search_fields = ("title", "description")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)