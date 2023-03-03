# flake8: noqa
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='Escreva sua biografia.',
                           max_length=1000, blank=True)

    def __str__(self):
        return self.author.username
