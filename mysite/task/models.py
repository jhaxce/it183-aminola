from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.OneToOneField(Token, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            token, created = Token.objects.get_or_create(user=self.user)
            self.token = token
        super().save(*args, **kwargs)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    tag = models.CharField(max_length=50, blank=True)
    is_priority = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
