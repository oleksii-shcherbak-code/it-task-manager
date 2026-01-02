from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import AVATAR_CHOICES

class AvatarChangeView(LoginRequiredMixin, TemplateView):
    template_name = "avatar_change.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatars"] = [choice[0] for choice in AVATAR_CHOICES]
        return context

    def post(self, request, *args, **kwargs):
        avatar = request.POST.get("avatar")
        if avatar:
            request.user.avatar = avatar
            request.user.save()
        return self.get(request, *args, **kwargs)
