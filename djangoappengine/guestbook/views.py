from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import SignForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from google.appengine.api import users

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME

import urllib

class MainPage(TemplateView):
    template_name = "guestbook/main_page.html"

    def get(self, request):
        # import logging
        # logging.warning("===== main %r", request)

        form = SignForm()
        # guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        # greetings_obj = Greeting()
        # greetings = greetings_obj.get_10_latest_message(guestbook_name)


        if users.get_current_user():
            url = users.create_logout_url(request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(request.get_full_path())
            url_linktext = 'Login'
        import logging
        logging.warning("===== sign %r", url_linktext)
        # context = {
        #     'greetings': greetings,
        #     'guestbook_name': guestbook_name,
        #     'url': url,
        #     'url_linktext': url_linktext,
        #     'form': form
        # }
        context = self.get_context_data(request)
        context['url'] = url
        context['url_linktext'] = url_linktext
        context['form'] = form

        import logging
        logging.error('template %s' % context)
        return render(request, self.template_name, context)

    def get_context_data(self, request, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greetings_obj = Greeting()
        greetings = greetings_obj.get_10_latest_message(guestbook_name)
        context['greetings'] = greetings
        context['guestbook_name'] = guestbook_name
        return context

class SignPost(FormView):
    template_name = "guestbook/main_page_form.html"

    def post(self, request, **kwargs):
        # import logging
        # logging.warning("===== sign %r", request)
        if request.method == 'POST':
            form = SignForm(request.POST)
            if form.is_valid():
                guestbook_name = request.POST.get('guestbook_name')
                greetings_obj = Greeting()
                greeting = greetings_obj.get_greetings_object(guestbook_name)
                if users.get_current_user():
                    greeting.author = users.get_current_user()

                greeting.content = request.POST.get('content')
                greeting.put()
                context = self.get_context_data(**kwargs)
                context['form'] = form
                # import logging
                # logging.warning("===== sign %r", context['guestbook_name'])
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