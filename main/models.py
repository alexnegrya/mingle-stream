from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_url = models.URLField(blank=True, null=True, default='https://i.ibb.co/N1kFxGn/user.png')
