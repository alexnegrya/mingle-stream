from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse
)
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.shortcuts import render, redirect
from main.models import User
from .models import Chats, ChatsMembers, Messages
from .serializers import ChangeChatSerializer


class AppView(ViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    template_name = 'app.html'
    authentication_classes = [SessionAuthentication]

    def _return_response(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def __getattr__(self, name):
        if name in ('post', 'patch', 'delete'):
            return self._return_response
        return super().__getattribute__(name)

    def get(self, request, *args, **kwargs):
        user_chats = Chats.objects.filter(owner=request.user)
        return render(request, self.template_name, {
            'avatar': request.user.img_url,
            'user_chats': [chat.to_dict() for chat in user_chats],
            'chats_members': {chat.id: ChatsMembers.objects.filter(
                chat=chat) for chat in user_chats}
        })


class ChatsView(ViewSet):
    http_method_names = ['post', 'patch', 'delete']
    authentication_classes = [SessionAuthentication]

    def create_chat(self, request, *args, **kwargs):
        Chats.objects.create(
            owner=request.user, title=request.data['title'])
        return redirect('app:app_page')

    def update_chat(self, request, *args, **kwargs):
        serializer = ChangeChatSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            try:
                chat = Chats.objects.get(id=serializer.data['chat_id'])
                for field in ('title', 'img_url', 'description', 'bg_url'):
                    if field in serializer.data:
                        setattr(chat, field, serializer.data[field])
                chat.save()
                return redirect('app:app_page')
            except KeyError:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()

    def delete_chat(self, request, *args, **kwargs):
        Chats.objects.get(id=request.data['chat_id']).delete()
        return HttpResponse()


class ChatMembersView(ViewSet):
    def get_chat_members_usernames(self, request, *args, **kwargs):
        return JsonResponse(list(ChatsMembers.objects.filter(
            chat__id=request.query_params['chat_id']).values_list(
                'user__username', flat=True)), safe=False)

    def add_chat_member(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data['username'])
            chat = Chats.objects.get(id=request.data['chat_id'])
            if ChatsMembers.objects.filter(user=user, chat=chat).count() < 1:
                ChatsMembers.objects.create(user=user, chat=chat)
            return HttpResponse()
        except User.DoesNotExist:
            return HttpResponse(status=404)

    def remove_chat_member(self, request, *args, **kwargs):
        ChatsMembers.objects.get(user__username=request.data['username']).delete()
        return HttpResponse()
    

class MessagesView(ViewSet):
    def get_chat_messages(self, request, *args, **kwargs):
        return JsonResponse([obj.to_dict() for obj in Messages.objects.filter(
            chat=Chats.objects.get(id=request.GET['chat_id']))],
            safe=False)
    
    def _update_message_data(self, message: Messages, request):
        for field in ('text',):
            if field in request.data:
                setattr(message, field, request.data[field])
                message.save()
                break
    
    def create_message(self, request, *args, **kwargs):
        message = Messages.objects.create(user=request.user,
            chat=Chats.objects.get(id=request.data['chat_id']))
        self._update_message_data(message, request)
        return HttpResponse(status=201)
    
    def update_message(self, request, *args, **kwargs):
        message = Messages.objects.get(id=request.data['message_id'])
        self._update_message_data(message, request)
        return HttpResponse()
    
    def delete_message(self, request, *args, **kwargs):
        Messages.objects.get(id=request.data['message_id']).delete()
        return HttpResponse()
