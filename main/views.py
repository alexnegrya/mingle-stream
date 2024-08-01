from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login
from .models import User
from .forms import *


class UserListView(ListView):
    http_method_names = ['post']
    model = User

    def post(self, request, *args, **kwargs):
        if UserAuthForm(request.POST).is_valid():
            user, is_created = User.objects.get_or_create(
                username=request.POST['username'],
                password=request.POST['password']
            )
            login(request, user)
            return HttpResponse(status=201 if is_created else 200)
        else:
            return HttpResponseBadRequest()
