from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from utils.forms import FormExtraClassMixin


class LoginForm(FormExtraClassMixin, forms.Form):
    """ Login form """
    email = forms.CharField(
        max_length=200,
        required=True,
        label=_("E-mail"),
        widget=forms.TextInput(
            attrs={'autocomplete': 'off'}
        )
    )
    password = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password'}
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if any(self._errors):
            return cleaned_data

        user = authenticate(
            email=cleaned_data['email'], password=cleaned_data['password'],
            request=self.request
        )
        if not user:
            self.add_error(None, _("Invalid Login Credentials"))

        if user and not user.is_active:
            self.add_error(None, _("Your account is not active."))

        return cleaned_data

    def handle(self, request):
        cleaned_data = self.cleaned_data
        user = authenticate(
            email=cleaned_data['email'],
            password=cleaned_data['password'],
            request=self.request
        )
        if user:
            login(request, user)
            return user


class RegisterForm(FormExtraClassMixin, forms.ModelForm):
    """ Registration form """

    email = forms.EmailField(
        max_length=200,
        required=True,
    )
    password = forms.CharField(
        max_length=200,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(),
    )
    confirm_password = forms.CharField(
        max_length=200,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        if any(self._errors):
            return cleaned_data

        if User.objects.filter(email__iexact=cleaned_data['email']).exists():
            self.add_error('email', _("This email is already exists."))

        if cleaned_data['password'] != cleaned_data['confirm_password']:
            self.add_error('password', _("Password does not match."))
        elif len(cleaned_data['password']) < 8:
            self.add_error('password', _("Password must be at least 8 characters."))

        return cleaned_data

    def save(self, *args, **kwargs):
        cleaned_data = self.cleaned_data

        # create user
        user = User(
            username=cleaned_data['email'],
            email=cleaned_data['email'],
            is_active=False
        )

        user.set_password(cleaned_data['password'])
        user.save()

        return user
