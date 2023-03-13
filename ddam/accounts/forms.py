from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import CustomUser


class CustomUserCreationForm(BaseUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email"]
