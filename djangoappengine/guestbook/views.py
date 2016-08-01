from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .forms import SignForm
from google.appengine.api import users

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME

import urllib

class MainPage(generic.base.TemplateView):
    template_name = "guestbook/main_page.html"

    def get(self, request):
        # import logging
        # logging.warning("===== main %r", request)
        guestbook_name = request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)

        # Ancestor Queries, as shown here, are strongly consistent with the High
        # Replication Datastore. Queries that span entity groups are eventually
        # consistent. If we omitted the ancestor from this query there would be
        # a slight chance that Greeting that had just been written would not
        # show up in a query.et
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(request.get_full_path())
            url_linktext = 'Login'
        import logging
        logging.warning("===== sign %r", url_linktext)
        template_values = {
            'greetings': greetings,
            'guestbook_name': guestbook_name,
            'url': url,
            'url_linktext': url_linktext,
        }
        import logging
        logging.error('template %s' % template_values)
        return render(request, self.template_name, template_values)

class SignPost(generic.edit.FormView):
    template_name = "guestbook/main_page.html"

    def post(self, request):
        # import logging
        # logging.warning("===== sign %r", request)
        if request.method == 'POST':

            guestbook_name = request.POST.get('guestbook_name')
            greeting = Greeting(parent=guestbook_key(guestbook_name))

            if users.get_current_user():
                greeting.author = users.get_current_user()

            greeting.content = request.POST.get('content')
            greeting.put()
            return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
            # return render(request, self.template_name, {'form': form})

        return HttpResponseRedirect('/')