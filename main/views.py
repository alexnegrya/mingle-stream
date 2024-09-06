from django.views.generic import View
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError
)
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings
import os
import imgbbpy
from app.funcs import change_model_image
from .models import User
from .forms import *


class MainView(View):
    http_method_names = ['get']
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AuthView(View):
    http_method_names = ['post']
    model = User

    def post(self, request, *args, **kwargs):
        if UserAuthForm(request.POST).is_valid():
            is_user_created = True
            try:
                user = User.objects.get(username=request.POST['username'])
                if authenticate(request, username=request.POST['username'],
                  password=request.POST['password']):
                    is_user_created = False
                else:
                    return HttpResponse(status=401)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=request.POST['username'],
                    password=request.POST['password']
                )
            login(request, user)
            print(f'User "{request.POST["username"]}" {"registered" if is_user_created else "logged in"}.')
            return redirect('app:app_page')
        else:
            return HttpResponseBadRequest()


class UploadImageView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        filename = request.FILES['image'].name
        with open(filename, 'wb+') as file:
            for chunk in request.FILES['image'].chunks():
                file.write(chunk)
        imgbb = imgbbpy.SyncClient(settings.IMGBB_API_KEY)
        # 31 days expiration
        image = imgbb.upload(file=filename, name=filename, expiration=2678400)
        if os.path.isfile(filename): os.remove(filename)
        change_model_image(request.POST['model'], image.url, request=request)
        return redirect('app:app_page')
