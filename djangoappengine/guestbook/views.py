from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import ndb

from .forms import SignForm, EditGreetingForm
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
        context['user_login'] = users.get_current_user()
        context['is_user_admin'] = users.is_current_user_admin()
        guestbook_name = self.request.GET.get('guestbook_name', Guestbook.get_default_name())
        guestbook = Guestbook(guestbook_name)
        greetings = guestbook.get_lastest_greeting(10)
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
        guestbook_obj = Guestbook(guestbook_name)
        guestbook_obj.put_greeting(content, author, users.get_current_user(), 'Email title')
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


class EditFormView(FormView):
    template_name = "guestbook/edit_form.html"
    form_class = EditGreetingForm
    success_url = "/"

    def form_valid(self, form):
        guestbook_name = self.request.POST.get('guestbook_name')
        greeting_id = self.request.POST.get('greeting_id')
        before_edit = self.request.POST.get('greeting_content')
        author = None
        if users.get_current_user():
            author = users.get_current_user()
        form.update_greeting()
        guestbook_name = form.cleaned_data['guestbook_name']
        self.success_url = '/?' + urllib.urlencode({'guestbook_name': guestbook_name})
        return super(EditFormView, self).form_valid(form)

    def form_invalid(self, form):
        greeting_id = self.request.POST.get('greeting_id')
        obj = ndb.Key('Guestbook', 'default_guestbook', Greeting, int(greeting_id)).get()
        data = {'greeting_author': self.request.POST.get('greeting_author'),
                'greeting_id': greeting_id,
                'greeting_content': obj.content,
                'guestbook_name': self.request.POST.get('guestbook_name')}
        my_form = EditGreetingForm(data)
        return self.render_to_response(self.get_context_data(form=my_form))


class DeleteFormView(FormView):
    template_name = "guestbook/delete_form.html"
    form_class = EditGreetingForm
    success_url = "/"


    def form_valid(self, form):
        guestbook_name = self.request.POST.get('guestbook_name')
        greeting_id = self.request.POST.get('greeting_id')
        author = None
        if users.get_current_user():
            author = users.get_current_user()
        form.delete_message_form()
        guestbook_name = form.cleaned_data['guestbook_name']
        self.success_url = '/?' + urllib.urlencode({'guestbook_name': guestbook_name})
        return super(DeleteFormView, self).form_valid(form)


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))