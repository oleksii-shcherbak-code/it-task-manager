from django.views.generic import CreateView, UpdateView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from tasks.forms import WorkerCreationForm, WorkerChangeForm
from tasks.models import Worker

class RegisterView(CreateView):
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = self.request.build_absolute_uri(f"/activate/{uid}/{token}/")
        send_mail("Activate your account", f"Click here:\n{activation_link}", "test@example.com", [user.email])
        messages.info(self.request, "Registration successful. Check your email for the activation link.")
        return redirect("login")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Worker.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Worker.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "✅ Your account has been activated. You can now log in.")
            return redirect("login")
        messages.error(request, "❌ Activation link is invalid or expired.")
        return redirect("register")

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = WorkerChangeForm
    template_name = "profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user
