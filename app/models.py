from django.db import models
from main.models import User
from .validators import validate_hex_str
from .funcs import get_random_hex_color


class Chats(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    color = models.CharField(max_length=6, null=False, blank=False,
        validators=[validate_hex_str], default=get_random_hex_color)
    img_url = models.URLField(null=False, blank=False, default='https://i.ibb.co/Pc1nGqJ/placeholder.png')
    description = models.TextField(null=True, blank=True)
    bg_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False,
        auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name_plural = 'chats'
    

class ChatsMembers(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=False, blank=False)
    chat = models.ForeignKey(Chats, models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'chats members'
