from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Competition(models.Model):
    name = models.CharField(max_length=100)
    teamsize = models.IntegerField()
    description = models.TextField()
    image = models.CharField(max_length=100, blank=True, null=True, default='https://picsum.photos/200/300')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competitions')
    applied_users = models.ManyToManyField(User, related_name='applied_users', blank=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name