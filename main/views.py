from django.views.generic import View
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse
)
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings
import os
import subprocess
from base64 import b64encode
import json
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
        image_base64 = b64encode(
            open(filename, 'rb').read()).decode('ascii')
        command = f'curl --location --request POST \
            "https://api.imgbb.com/1/upload?expiration=2678400&key={settings.IMGBB_API_KEY}" \
            --form "image={image_base64}"'
        os.system(command)
        res = json.loads(subprocess.check_output(command, shell=True))
        if res.get('status') == 200 and res.get('success'):
            if os.path.isfile(filename): os.remove(filename)
            change_model_image(request.POST['model'], res['data']['url'], request=request)
            return redirect('app:app_page')
        else:
            return HttpResponseServerError()
