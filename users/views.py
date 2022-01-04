from django.shortcuts import render
from django.views.generic import CreateView
from learning_logs.forms import CustomUserCreationForm
from django.urls import reverse_lazy
# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'
