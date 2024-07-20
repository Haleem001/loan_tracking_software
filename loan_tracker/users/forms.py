from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import random
import string

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'email')



class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def generate_username(self, first_name, last_name):
        base_username = f"{first_name[0].lower()}.{last_name.lower()}"
        username = base_username
        counter = 1

        # Ensure the username is unique
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        return username

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.generate_username(self.cleaned_data['first_name'], self.cleaned_data['last_name'])
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Generate a random password
        user.set_password(password)
        user.email_user(
            subject="Welcome!",
            message=f"Your new account has been created. Your username is: {user.username} and your password is: {password}\n\n\n Don't forget to change your password after logging in. \n\n\n Thank You!! ",
            from_email="your_email@example.com"
        )
        if commit:
            user.save()
        return user
