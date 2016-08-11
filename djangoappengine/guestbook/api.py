from django.http import HttpResponse
from django.views.generic import FormView
from django.core import serializers
import ast

from google.appengine.datastore.datastore_query import Cursor

from guestbook.models import Guestbook

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
    def get(self, request, *args, **kwargs):
        import logging
        try:
            guestbook_name = kwargs['guestbook_name']
            guestbook = Guestbook(guestbook_name)
            data = guestbook.convert_list_to_dict()
            json_data = json.dumps(data)
            logging.warn("%r" % json_data)
            # return JsonResponse(json_data)
            return HttpResponse(json_data, content_type="application/json")
        except:
            return HttpResponse(status=404)