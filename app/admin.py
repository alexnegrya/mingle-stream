from django.contrib import admin
from .models import Chats, ChatsMembers


@admin.register(Chats)
class ChatsAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatsMembers)
class ChatsMembersAdmin(admin.ModelAdmin):
    pass
