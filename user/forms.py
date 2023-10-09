from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    error_messages = {
        "first_name_is_missing": _("First name is a mandatory field."),
        "last_name_is_missing": _("Last name is a mandatory field."),
        "email_is_missing": _("Email is a mandatory field."),
        "password_mismatch": _("The two password fields didn’t match."),
    }
    first_name = forms.CharField(
        label=_("First Name"),
        strip=True,
        widget=forms.TextInput(attrs={"title": _("First Name")}),
        help_text=_("Enter your first name."),
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        strip=True,
        widget=forms.TextInput(attrs={"title": _("Last Name")}),
        help_text=_("Enter your last name."),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={"title": _("Email")}),
        help_text=_("Enter your email address."),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        field_classes = {"username": UsernameField, "email": EmailField}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name(self.cleaned_data["first_name"])
        user.last_name(self.cleaned_data["last_name"])
        user.email(self.cleaned_data["email"])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
