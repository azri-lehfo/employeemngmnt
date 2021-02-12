from django.views.generic import TemplateView, View, FormView, CreateView
from django.contrib.auth import logout
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import LoginForm, RegisterForm


class IndexView(TemplateView):
    """ Index view. """
    template_name = 'index.html'


class LoginView(FormView):
    """ Login page """
    template_name = 'auths/login.html'
    form_class = LoginForm

    def get(self, *args, **kwargs):
        """ If already login, redirect to success url """
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        form.handle(self.request)

        messages.success(self.request, _("Successfully logged in."))

        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET['next']
        return reverse('index')


class LogoutView(View):
    """ Logout """

    def get(self, request, *args, **kwargs):
        logout(request)

        messages.success(self.request, _("Successfully logged out."))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class RegistraterView(CreateView):
    """ Register """
    template_name = 'auths/register.html'
    form_class = RegisterForm

    def get_success_url(self):
        messages.success(self.request, _("Succesful register."))
        return reverse('auths:login')
