from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Message

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'role', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        # Allow empty credentials for admin code login
        if not username and not password:
            return self.cleaned_data
        
        # For regular login, both fields are required
        if not username:
            raise ValidationError("Email is required.")
        if not password:
            raise ValidationError("Password is required.")
        
        return super().clean()

class MessageForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your message to your doctor...',
            'rows': 3
        }),
        label='Message',
        max_length=1000,
        required=True
    )
    
    class Meta:
        model = Message
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text or not text.strip():
            raise ValidationError("Message cannot be empty.")
        return text.strip()

class DoctorReplyForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your reply to the patient...',
            'rows': 2
        }),
        label='Reply',
        max_length=1000,
        required=True
    )
    
    class Meta:
        model = Message
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text or not text.strip():
            raise ValidationError("Reply cannot be empty.")
        return text.strip()