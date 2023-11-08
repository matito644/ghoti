from django.contrib.auth.forms import UserCreationForm

from webpage.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
