from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from .models import User
from .forms import *


class MainListView(ListView):
    http_method_names = ['get']
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserListView(ListView):
    http_method_names = ['post']
    model = User

    def post(self, request, *args, **kwargs):
        if UserAuthForm(request.POST).is_valid():
            try:
                user = User.objects.get(username=request.POST['username'])
                if authenticate(request, username=request.POST['username'], password=request.POST['password']):
                    status_code = 200
                else:
                    return HttpResponse(status=401)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=request.POST['username'],
                    password=request.POST['password']
                )
                status_code = 201
            login(request, user)
            return HttpResponse(status=status_code)
        else:
            return HttpResponseBadRequest()
