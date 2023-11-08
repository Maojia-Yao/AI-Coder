from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Define a custom form that inherits from UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    # Add an email field to the form, make it required, and use a custom widget
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input-item'}))

    class Meta:
        # Specify the model that the form is for (User model)
        model = User
        # Define the fields that will be included in the form
        fields = ('username', 'email', 'password1', 'password2')
