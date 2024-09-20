from django.views.generic import View
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse
)
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import render
from main.models import User
from .models import Chats, ChatsMembers, Messages


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class AppView(View):
    http_method_names = ['get']
    template_name = 'app.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'avatar': request.user.img_url
        })


class ChatsView(ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_user_chats(self, request, *args, **kwargs):
        return JsonResponse([obj.to_dict() for obj in Chats.objects.filter(
            owner=request.user)], safe=False)

    def create_chat(self, request, *args, **kwargs):
        Chats.objects.create(
            owner=request.user, title=request.data['title'])
        return HttpResponse(status=201)

    def update_chat(self, request, *args, **kwargs):
        chat = Chats.objects.get(id=request.data['chat_id'])
        for field in ('title', 'img_url', 'description', 'bg_url'):
            if field in request.data:
                setattr(chat, field, request.data[field])
        chat.save()
        return HttpResponse()

    def delete_chat(self, request, *args, **kwargs):
        Chats.objects.get(id=request.data['chat_id']).delete()
        return HttpResponse()


class ChatMembersView(ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_chat_members_usernames(self, request, *args, **kwargs):
        return JsonResponse(list(ChatsMembers.objects.filter(
            chat__id=request.query_params['chat_id']).values_list(
                'user__username', flat=True)), safe=False)

    def add_chat_member(self, request, *args, **kwargs):
        ChatsMembers.objects.create(
            chat=Chats.objects.get(id=request.data['chat_id']),
            user=User.objects.get(username=request.data['username'])
        )
        return HttpResponse(status=201)

    def remove_chat_member(self, request, *args, **kwargs):
        ChatsMembers.objects.get(user__username=request.data['username']).delete()
        return HttpResponse()
    

class MessagesView(ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

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
