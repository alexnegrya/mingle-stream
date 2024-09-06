from django.views.generic import View
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse
)
from django.shortcuts import render


class AppView(View):
    http_method_names = ['get']
    template_name = 'app.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'avatar': request.user.img_url
        })
