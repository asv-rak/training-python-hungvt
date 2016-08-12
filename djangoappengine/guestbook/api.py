from django.http import HttpResponse
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api import users

from guestbook.models import Guestbook, Greeting

from .forms import PostNewMessageForm

import json


class JsonResponse(HttpResponse):
    def __init__(self, content={}, mimetype=None, status=None,
             content_type='application/json'):
        super(JsonResponse, self).__init__(json.dumps(content), mimetype=mimetype,
                                           status=status, content_type=content_type)


class APIGreetingDetail(FormView):
    def get(self, request, *args, **kwargs):
        import logging
        try:
            guestbook_name = kwargs['guestbook_name']
            id = kwargs['id']
            guestbook = Guestbook(guestbook_name)
            data = guestbook.get_item_by_id(id).convert_item_to_dict()
            json_data = json.dumps(data)
            # return JsonResponse(json_data)
            return HttpResponse(json_data, content_type="application/json")
        except:
            return HttpResponse(status=404)


class APIGreeting(FormView):
    success_url = "/"
    form_class = PostNewMessageForm

    def get(self, request, *args, **kwargs):
        try:
            guestbook_name = kwargs['guestbook_name']
            guestbook = Guestbook(guestbook_name)
            data = guestbook.convert_list_to_dict()
            json_data = json.dumps(data)
            # return JsonResponse(json_data)
            return HttpResponse(json_data, content_type="application/json")
        except:
            return HttpResponse(status=404)


    def form_valid(self, form):
        print "valid method"
        guestbook_name = form.cleaned_data.get('guestbook_name')
        greeting_content = form.cleaned_data.get('greeting_content')
        author = users.get_current_user()
        guestbook = Guestbook(guestbook_name)
        result = guestbook.put_greeting(greeting_content, author, author, 'Email title')
        if result:
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=404)


    def form_invalid(self, form):
        return HttpResponse(status=400)

