from django import forms
from django.contrib.auth.forms import UserCreationForm
from account_manager.models import Account
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text='Required. Inform a valid email address.', required=True)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', )


class LogInForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class UpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                Account.objects.exclude(
                    pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError(
                'Email "%s" is already in use.' % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                Account.objects.exclude(
                    pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(
                'Username "%s" is already in use.' % username)
