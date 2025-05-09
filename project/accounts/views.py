from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login

from accounts.forms import RegisterForm, LoginForm


class AuthSuccessUrlMixin:
    def get_success_url(self):
        next_url = self.request.GET.get('next')

        if not next_url:
            next_url = self.request.POST.get('next')

        if not next_url:
            next_url = reverse('main')

        return next_url


class UserRegisterView(AuthSuccessUrlMixin, FormView):
    template_name = 'registration.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())


class UserLoginView(AuthSuccessUrlMixin, LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')
