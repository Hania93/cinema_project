# Create your views here.

from .forms import RegisterForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")