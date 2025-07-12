from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrator'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_approved_doctor = models.BooleanField(default=False, help_text="Whether doctor account is approved")
    date_joined = models.DateTimeField(auto_now_add=True)
    # New: doctor assignment for patients
    assigned_doctor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'doctor'}, related_name='patients')
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        # Auto-approve patients, require manual approval for doctors
        if self.role == 'patient':
            self.is_approved_doctor = True  # Not applicable but set for consistency
        elif self.role == 'doctor' and not self.pk:
            # New doctor accounts need approval
            self.is_approved_doctor = False
        elif self.role == 'admin':
            self.is_staff = True
            self.is_approved_doctor = True
        
        super().save(*args, **kwargs)
    
    @property
    def is_approved(self):
        """Check if user is approved to access the system"""
        if self.role == 'patient':
            return True
        elif self.role == 'doctor':
            return self.is_approved_doctor
        elif self.role == 'admin':
            return True
        return False

# Messaging between patient and doctor
class Message(models.Model):
    sender = models.ForeignKey('CustomUser', related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey('CustomUser', related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.get_full_name()} to {self.receiver.get_full_name()} at {self.timestamp}"