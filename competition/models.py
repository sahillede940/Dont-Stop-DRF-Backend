from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.


class Competition(models.Model):
    name = models.CharField(max_length=100)
    teamsize = models.IntegerField()
    description = models.TextField()
    image = models.CharField(max_length=100, blank=True, null=True, default='https://picsum.photos/200/300')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competition_owner')
    applied_users = models.ManyToManyField(User, related_name='competition_applied_users', blank=True)
    location = models.CharField(max_length=100, default="IIT Kharagpur")
    deadline = models.DateTimeField(default=timezone.now())

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name