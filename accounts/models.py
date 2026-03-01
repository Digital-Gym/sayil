from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with bio and favorite routes."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(
        upload_to='avatars/', blank=True, null=True
    )
    favorite_routes = models.ManyToManyField(
        'routes.Route', related_name='favorited_by', blank=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'
