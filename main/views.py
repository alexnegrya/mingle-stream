from django.views.generic import ListView
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse
)
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.conf import settings
import os
import subprocess
from base64 import b64encode
import json
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


class UploadImageView(ListView):
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
            os.remove(filename)
            return JsonResponse({'url': res['data']['url']})
        else:
            return HttpResponseServerError()
