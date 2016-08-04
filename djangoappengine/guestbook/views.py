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

class MainPageView(TemplateView):
    template_name = "guestbook/main_page.html"

    def get_context_data(self, **kwargs):
        form = SignForm()
        if users.get_current_user():
            url = users.create_logout_url(self.request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.get_full_path())
            url_linktext = 'Login'
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['url'] = url
        context['url_linktext'] = url_linktext
        context['form'] = form
        guestbook_name = self.request.GET.get('guestbook_name', Guestbook.get_default_name())
        guestbook = Guestbook()
        greetings = guestbook.get_lastest_greeting(guestbook_name, 10)
        context['greetings'] = greetings
        context['guestbook_name'] = guestbook_name
        return context

class SignPostView(FormView):
    template_name = "guestbook/main_page_form.html"
    success_url = "/"
    form_class = SignForm

    def form_valid(self, form):
        guestbook_name = self.request.POST.get('guestbook_name')
        content = self.request.POST.get('content')
        author = None
        if users.get_current_user():
            author = users.get_current_user()
        guestbook_obj = Guestbook()
        guestbook_obj.put_greeting(guestbook_name, content, author)
        guestbook_obj.sendmail(users.get_current_user(), 'Email title', author)
        # return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
        return super(SignPostView, self).form_valid(form)

    def form_invalid(self, form):
        context = {}
        context['error_message'] = "Length is not valid"
        return self.render_to_response(context)

class MailView(View):

    @ndb.transactional
    def get(self, request, *args, **kwargs):
        title = request.GET.get('title')
        author = request.GET.get('author')
        mail.send_mail(author, 'hungvt@aoi-sys.vn', title, """vi du noi dung""")
        return HttpResponseRedirect('/')