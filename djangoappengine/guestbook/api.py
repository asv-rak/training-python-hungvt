from django.http import HttpResponse
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api import users

from guestbook.models import Guestbook, Greeting

from .forms import PostNewMessageForm

import json


class JsonResponseMixin(object):
    def render_to_response(self, data):
        json_data=json.dumps(data)
        return HttpResponse(json_data, content_type="application/json")


class APIGreetingDetail(JsonResponseMixin, FormView):
    form_class = PostNewMessageForm

    #       GET http://localhost:8080/api/guestbook/name_of_guestbook/greeting/id_of_greeting
    #
    #       return data of the greeting in json string
    #
    #       return Http 404 if query error
    def get(self, request, *args, **kwargs):
        try:
            guestbook_name = kwargs['guestbook_name']
            id = kwargs['id']
            guestbook = Guestbook(guestbook_name)
            data = guestbook.get_item_by_id(id).convert_item_to_dict()
            return self.render_to_response(data)
        except:
            return HttpResponse(status=404)


    #       PUT http://localhost:8080/api/guestbook/name_of_guestbook/greeting/id_of_greeting
    #
    #       return Http 200 if edited successfully
    #
    #       return Http 404 if query error
    def put(self, request, *args, **kwargs):
        # # request.body
        # # {
        # #     "greeting_content": "asda",
        # #     "guestbook_name": "default_guestbook"
        # # }
        request.POST = json.loads(request.body)
        return super(APIGreetingDetail, self).put(request, *args, **kwargs)

    #       PUT http://localhost:8080/api/guestbook/name_of_guestbook/greeting/id_of_greeting
    #
    #       return Http 200 if edited successfully
    def form_valid(self, form):
        self.request.POST = json.loads(self.request.body)
        guestbook_name = self.kwargs['guestbook_name']
        content = self.request.POST.get('greeting_content')
        id = self.kwargs['id']
        guestbook = Guestbook(guestbook_name)
        guestbook.update_greeting_by_id(users.get_current_user(), users.get_current_user(), False, id, content)
        return HttpResponse(status=200)

    #       PUT http://localhost:8080/api/guestbook/name_of_guestbook/greeting/id_of_greeting
    #
    #       return Http 404 if query error
    def form_invalid(self, form):
        return HttpResponse(status=404)

    #       DELETE http://localhost:8080/api/guestbook/name_of_guestbook/greeting/id_of_greeting
    #
    #       return Http 200 if deleted successfully
    #
    #       return Http 404 if query error
    def delete(self, request, *args, **kwargs):
        guestbook_name = kwargs['guestbook_name']
        id = kwargs['id']
        guestbook = Guestbook(guestbook_name)
        result = guestbook.delete_message(users.get_current_user(), users.get_current_user(), False, id)
        if result:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)



class APIGreeting(JsonResponseMixin, FormView):
    success_url = "/"
    form_class = PostNewMessageForm

    #       GET http://localhost:8080/api/guestbook/name_of_guestbook/greeting/
    #
    #       return list data of the greetings of a guestbook in json string
    #
    #       return Http 404 if query error
    def get(self, request, *args, **kwargs):
        try:
            guestbook_name = kwargs['guestbook_name']
            guestbook = Guestbook(guestbook_name)
            data = guestbook.convert_list_to_dict()
            return self.render_to_response(data)
        except:
            return HttpResponse(status=404)


    #       POST http://localhost:8080/api/guestbook/name_of_guestbook/greeting/
    #
    #       return Http 200 if a new greeting is added successfully
    #
    #       return Http 404 if query error
    def form_valid(self, form):
        guestbook_name = form.cleaned_data.get('guestbook_name')
        greeting_content = form.cleaned_data.get('greeting_content')
        author = users.get_current_user()
        guestbook = Guestbook(guestbook_name)
        result = guestbook.put_greeting(greeting_content, author, author, 'Email title')
        if result:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)

    #       POST http://localhost:8080/api/guestbook/name_of_guestbook/greeting/
    #
    #       return Http 400 if form invalid
    def form_invalid(self, form):
        return HttpResponse(status=400)