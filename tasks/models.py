from django.db import models
from django.contrib.auth.models import AbstractUser

# --- Avatar choices ---
AVATAR_CHOICES = [
    ("avatar1.svg", "Avatar 1"),
    ("avatar2.svg", "Avatar 2"),
    ("avatar3.svg", "Avatar 3"),
    ("avatar4.svg", "Avatar 4"),
    ("avatar5.svg", "Avatar 5"),
    ("avatar6.svg", "Avatar 6"),
    ("avatar7.svg", "Avatar 7"),
    ("avatar8.svg", "Avatar 8"),
    ("avatar9.svg", "Avatar 9"),
    ("avatar10.svg", "Avatar 10"),
]


class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, blank=True
    )

    avatar = models.CharField(
        max_length=30, choices=AVATAR_CHOICES, default="avatar1.svg"
    )

    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name = "Task Type"
        verbose_name_plural = "Task Types"

    def __str__(self):
        return self.name


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignee = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["is_completed", "deadline", "-priority"]

    def __str__(self):
        return f"{self.title} [{self.priority}]"
