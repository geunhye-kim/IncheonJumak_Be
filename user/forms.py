from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.forms import ValidationError
from user.models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
        # field_classes = {"username": UsernameField}
        
    def clean_username(self):
        username = self.cleaned_data.get("email")
        if (
            username
            and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return username