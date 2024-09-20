from django.db import models
from main.models import User
from .validators import validate_hex_str
from .funcs import get_random_hex_color


class Chats(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    color = models.CharField(max_length=6, null=False, blank=False,
        validators=[validate_hex_str], default=get_random_hex_color)
    img_url = models.URLField(null=False, blank=False,
        default='https://i.ibb.co/Pc1nGqJ/placeholder.png')
    description = models.TextField(null=True, blank=True)
    bg_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False,
        auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name_plural = 'chats'

    def to_dict(self):
        return {f: getattr(self, f) for f in (
            'id', 'title', 'color', 'img_url', 'description', 'bg_url', 'created_at')}
    

class ChatsMembers(models.Model):
    user = models.ForeignKey(User, models.CASCADE, null=False, blank=False)
    chat = models.ForeignKey(Chats, models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'chats members'


class Messages(models.Model):
    chat_member = models.ForeignKey(ChatsMembers, models.CASCADE,
        null=False, blank=False)
    text = models.TextField(null=True, blank=True)
    img_url = models.URLField(null=True, blank=True)
    youtube_video_id = models.CharField(max_length=11, null=True, blank=True)
    file_url = models.URLField(null=True, blank=True)
    mixcloud_key = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(null=False, blank=False,
        auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name_plural = 'messages'

    def to_dict(self):
        d = {'id': self.id}
        d.update({'user_img_url': self.chat_member.user.img_url,
            'username': self.chat_member.user.username})
        d.update({f: getattr(self, f) for f in (
            'text', 'img_url', 'youtube_video_id', 'file_url', 'mixcloud_key',
            'created_at')})
        return d
