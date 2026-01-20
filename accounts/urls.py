from django.urls import path

from accounts.views.avatar_views import AvatarChangeView
from accounts.views.register_views import RegisterView
from accounts.views.activate_views import ActivateAccountView
from accounts.views.profile_views import ProfileView, ProfileUpdateView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate-account",
    ),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/avatar/", AvatarChangeView.as_view(), name="avatar-change"),
]
