from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class UserCreateView(generic.CreateView):
    model = get_user_model()
    form_class = UserCreationForm
    success_url = reverse_lazy('account:login')
    template_name = "registration/signup.html"

