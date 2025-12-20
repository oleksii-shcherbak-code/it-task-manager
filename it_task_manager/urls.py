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

from tasks.views import RegisterView, ProfileView, ProfileUpdateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),
    path("", include("tasks.urls")),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html"), name="password_change"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="password_reset"),
]
