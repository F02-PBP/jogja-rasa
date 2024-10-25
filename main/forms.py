from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.forms import ModelForm
from reservation.models import Reservation

class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=50,
        label='Nama Lengkap',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.EmailField(
        required=True,
        label='Alamat Email',
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    interested_in = forms.ChoiceField(
        choices=[('', 'Pilih Makanan Favorit')] + UserProfile.interested_food,
        label='Makanan Favorit',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = User
        fields = ('full_name', 'email', 'interested_in', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-input'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-input'})

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                interested_in=self.cleaned_data['interested_in']
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your password'})
    )