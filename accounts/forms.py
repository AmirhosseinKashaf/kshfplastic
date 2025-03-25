from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add the email field

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Include email in fields

class UsernameOrEmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean_username(self):
        username_or_email = self.cleaned_data.get('username')

        # Check if the input is an email
        User = get_user_model()
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                return user.username  # Return the username for authentication
            except User.DoesNotExist:
                raise ValidationError("This email is not registered.")
        
        # If it's not an email, assume it's a username
        try:
            user = User.objects.get(username=username_or_email)
            return username_or_email
        except User.DoesNotExist:
            raise ValidationError("This username does not exist.")
    
class ForgotPasswordForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email")

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data.get('username_or_email')

        # Check if the input is an email
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                raise ValidationError("This email is not registered.")
        else:
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                raise ValidationError("This username is not registered.")

        return user  # Return the user object
    
class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput)
