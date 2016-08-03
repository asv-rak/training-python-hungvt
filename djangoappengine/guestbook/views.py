from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import taskqueue

from guestbook.models import Greeting, Guestbook, guestbook_key, DEFAULT_GUESTBOOK_NAME

import urllib

class MainPage(TemplateView):
    template_name = "guestbook/main_page.html"

    def get_context_data(self, **kwargs):
        form = SignForm()
        if users.get_current_user():
            url = users.create_logout_url(self.request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.get_full_path())
            url_linktext = 'Login'
        context = super(MainPage, self).get_context_data(**kwargs)
        context['url'] = url
        context['url_linktext'] = url_linktext
        context['form'] = form
        guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        # greetings_obj = Greeting()
        # greetings = greetings_obj.get_10_latest_message(guestbook_name)
        guestbook = Guestbook()
        greetings = guestbook.get_lastest_greeting(guestbook_name, 10)
        context['greetings'] = greetings
        context['guestbook_name'] = guestbook_name
        return context

class SignPost(FormView):
    template_name = "guestbook/main_page_form.html"

    def post(self, request, **kwargs):
        if request.method == 'POST':
            form = SignForm(request.POST)
            if form.is_valid():
                guestbook_name = request.POST.get('guestbook_name')
                content = request.POST.get('content')
                author = None
                if users.get_current_user():
                    author = users.get_current_user()
                greetings_obj = Greeting()
                greetings_obj.add_new(guestbook_name, content, author)
                if users.get_current_user():
                    self.send_email()
                context = self.get_context_data(**kwargs)
                context['form'] = form
                # guestbook_name = request.POST.get('guestbook_name')
                # greetings_obj = Greeting()
                # greeting = greetings_obj.get_greetings_object(guestbook_name)
                # if users.get_current_user():
                #     greeting.author = users.get_current_user()
                #     self.send_email()
                # greeting.content = request.POST.get('content')
                # greeting.put()
                # context = self.get_context_data(**kwargs)
                # context['form'] = form
                return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
            else:
                context = super(SignPost, self).get_context_data(**kwargs)
                context['error_message'] = "Length is not valid"
                return render(request, self.template_name, context)
        else:
            # import logging
            # logging.warning("===== context %r", context)
            return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(SignPost, self).get_context_data(**kwargs)
        return context

    @ndb.transactional
    def send_email(self):
        message = mail.EmailMessage(sender='hungvt@aoi-sys.vn',
                                    to=users.get_current_user().email(),
                                    subject="Your account has been approved",
                                    body="""vi du noi dung""")
        message.send()