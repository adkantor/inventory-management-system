from django.contrib.auth.models import AbstractUser
from django.db.models import Q


class CustomUser(AbstractUser):

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



