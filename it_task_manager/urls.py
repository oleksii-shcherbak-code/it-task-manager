"""
URL configuration for it_task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from tasks.views import (
    # Index/Home
    IndexView,

    # Auth & Profile
    RegisterView, ProfileView, ProfileUpdateView,

    # Workers
    WorkerListView, WorkerDetailView,

    # Tasks
    TaskListView, TaskDetailView, TaskCreateView,
    TaskUpdateView, TaskDeleteView,

    # Task Types
    TaskTypeListView, TaskTypeDetailView,
    TaskTypeCreateView, TaskTypeUpdateView,
    TaskTypeDeleteView, TaskTypeAnalyticsView,

    # Search
    SearchView, search_suggest,

    # Avatar
    AvatarChangeView,

    # Task status
    toggle_task_status,
)

urlpatterns = [
    # Admin & Debug
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),

    # Index
    path("", IndexView.as_view(), name="index"),

    # Auth
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Profile
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"), name="password_change"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="password_reset"),

    # Workers
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),

    # Tasks
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    # Task Types
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/<int:pk>/", TaskTypeDetailView.as_view(), name="task-type-detail"),
    path("task-types/create/", TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", TaskTypeDeleteView.as_view(), name="task-type-delete"),
    path("task-types/analytics/", TaskTypeAnalyticsView.as_view(), name="task-type-analytics"),

    # Search
    path("search/", SearchView.as_view(), name="search"),
    path("search/suggest/", search_suggest, name="search-suggest"),

    # Avatar
    path("profile/avatar/", AvatarChangeView.as_view(), name="avatar-change"),

    # Task status
    path("tasks/<int:pk>/toggle/", toggle_task_status, name="task-toggle"),

]
