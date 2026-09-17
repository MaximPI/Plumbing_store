from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from django import forms

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Введите имя'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Введите пароль'}))
	class Meta:
		model = User
		fields = ('username', 'password')

class UserRegistrationForm(UserCreationForm):
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите почту'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}))
	class Meta:
		model = User
		fields = ('username', 'last_name', 'email', 'password1', 'password2')

class UserProfileForm(UserChangeForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4", "readonly": True}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4"}))
	phone_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control py-4"}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control py-4", "readonly": True}))
	class Meta:
		model = User
		fields = ('username', 'last_name', 'phone_number', 'email')
