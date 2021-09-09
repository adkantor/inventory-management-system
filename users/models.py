from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def statuses():
        result = []
        q_active=Q(is_active=True)
        users = CustomUser.objects.filter(q_active)
        for user in users:
            serialized = {
                'username': user.username,
                'is_authenticated': user.is_authenticated,
                'last_login': user.last_login
            }
            result.append(serialized)
        return result

    def __str__(self):
        return f'{self.last_name}, {self.first_name} | {self.email}  |  {self.username}'

    def get_absolute_url(self):
        return reverse('employee_detail', args=[str(self.id)])