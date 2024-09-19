from django.urls import path
from .views import *


urlpatterns = [
    path('', AppView.as_view(), name='app_page'),

    path('user-chats/', ChatsView.as_view({'get': 'get_user_chats'}), name='user_chats'),
    path('create-chat/', ChatsView.as_view({'post': 'create_chat'}), name='create_chat'),
    path('change-chat/', ChatsView.as_view({'patch': 'update_chat'}), name='change_chat'),
    path('delete-chat/', ChatsView.as_view({'delete': 'delete_chat'}), name='delete_chat'),

    path('chat-members/', ChatMembersView.as_view({'get': 'get_chat_members_usernames'}), name='chat_members'),
    path('add-chat-member/', ChatMembersView.as_view({'post': 'add_chat_member'}), name='add_chat_member'),
    path('delete-chat-member/', ChatMembersView.as_view({'delete': 'remove_chat_member'}), name='delete_chat_member')
]
