from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect

from accounts.forms import WorkerCreationForm


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
        activation_link = self.request.build_absolute_uri(
            f"/accounts/activate/{uid}/{token}/"
        )

        send_mail(
            "Activate your account",
            f"Click here:\n{activation_link}",
            "test@example.com",
            [user.email],
        )

        messages.info(self.request, "Registration successful. Check your email.")
        return redirect("login")
