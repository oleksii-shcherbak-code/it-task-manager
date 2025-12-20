from django.contrib import admin
from .models import Task, TaskType, Worker, Position


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "assignee", "task_type", "priority", "deadline", "is_completed")
    list_filter = ("priority", "is_completed", "task_type")
    search_fields = ("title", "description")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "position", "is_staff", "is_active")
    list_filter = ("position", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
