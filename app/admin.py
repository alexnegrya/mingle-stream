from django.contrib import admin
from .models import Chats, ChatsMembers, Messages


@admin.register(Chats)
class ChatsAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatsMembers)
class ChatsMembersAdmin(admin.ModelAdmin):
    pass


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    pass
