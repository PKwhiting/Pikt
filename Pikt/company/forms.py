from django import forms
from Authentication.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password']
        labels = {
            'username': False,
            'first_name': False,
            'last_name': False,
            'email': False,
            'phone_number': False,
            'role': False,
            'password': False,
        }
        help_texts = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': '',
            'role': '',
            'password': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Phone Number'}),
            'role': forms.Select(attrs={'class': 'text-field', 'style': 'width: 100%; height: 37px;'}),
            'password': forms.PasswordInput(attrs={'class': 'text-field w-input', 'style': 'width: 100%; margin-top: 8px;', 'placeholder': 'Password'}),
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user