from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignForm
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb

from guestbook.models import Greeting, Guestbook

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
        guestbook_name = self.request.GET.get('guestbook_name', Guestbook.get_default_name())
        # greetings_obj = Greeting()
        # greetings = greetings_obj.get_10_latest_message(guestbook_name)
        guestbook = Guestbook()
        greetings = guestbook.get_lastest_greeting(guestbook_name, 10)
        context['greetings'] = greetings
        context['guestbook_name'] = guestbook_name
        return context

class SignPost(FormView):
    template_name = "guestbook/main_page_form.html"
    success_url = "guestbook/main_page.html"

    def form_valid(self, request, form, **kwargs):
        guestbook_name = request.POST.get('guestbook_name')
        content = request.POST.get('content')
        author = None
        if users.get_current_user():
            author = users.get_current_user()
        # greetings_obj = Greeting()
        # greetings_obj.add_new(guestbook_name, content, author)
        guestbook_obj = Guestbook()
        guestbook_obj.put_greeting(guestbook_name, content, author)
        if users.get_current_user():
            # self.send_email()
            # add task to task queue
            guestbook_obj.sendmail()
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

    def form_invalid(self, form):
        context = {}
        context['error_message'] = "Length is not valid"
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = SignForm(request.POST)
            if form.is_valid():
                return self.form_valid(request, form, **kwargs)
            else:
                return self.form_invalid(form, **kwargs)
        else:
            return HttpResponseRedirect('/')

    # def post(self, request, **kwargs):
    #     if request.method == 'POST':
    #         form = SignForm(request.POST)
    #         if form.is_valid():
    #             guestbook_name = request.POST.get('guestbook_name')
    #             content = request.POST.get('content')
    #             author = None
    #             if users.get_current_user():
    #                 author = users.get_current_user()
    #             # greetings_obj = Greeting()
    #             # greetings_obj.add_new(guestbook_name, content, author)
    #             guestbook_obj = Guestbook()
    #             guestbook_obj.put_greeting(guestbook_name, content, author)
    #             if users.get_current_user():
    #                 # self.send_email()
    #                 # add task to task queue
    #                 guestbook_obj.sendmail()
    #             context = self.get_context_data(**kwargs)
    #             context['form'] = form
    #             # guestbook_name = request.POST.get('guestbook_name')
    #             # greetings_obj = Greeting()
    #             # greeting = greetings_obj.get_greetings_object(guestbook_name)
    #             # if users.get_current_user():
    #             #     greeting.author = users.get_current_user()
    #             #     self.send_email()
    #             # greeting.content = request.POST.get('content')
    #             # greeting.put()
    #             # context = self.get_context_data(**kwargs)
    #             # context['form'] = form
    #             return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
    #         else:
    #             context = super(SignPost, self).get_context_data(**kwargs)
    #             context['error_message'] = "Length is not valid"
    #             return render(request, self.template_name, context)
    #     else:
    #         # import logging
    #         # logging.warning("===== context %r", context)
    #         return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(SignPost, self).get_context_data(**kwargs)
        return context

class MailView(View):

    @ndb.transactional
    def get(self, request, *args, **kwargs):
        message = mail.EmailMessage(sender='hungvt@aoi-sys.vn',
                                    to='hungvt@aoi-sys.vn',
                                    subject="Your account has been approved",
                                    body="""vi du noi dung""")
        message.send()
        return HttpResponseRedirect('/')