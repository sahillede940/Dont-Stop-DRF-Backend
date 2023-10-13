from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = None
    fullName = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=[
                              True, 'Email already exists'])
    college = models.CharField(max_length=100)
    about = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    # exclude email from required fields
    REQUIRED_FIELDS = ['fullName', 'college', 'about']


class UserSelector(models.Model):
    user_applied = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applied_competition_user')
    competition = models.ForeignKey(
        'competition.Competition', on_delete=models.CASCADE, related_name='applied_competition')
    status = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
