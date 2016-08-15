from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt

from . import views, api

urlpatterns = [
    # Examples:
    # url(r'^$', 'Django_StandAlone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', views.MainPageView.as_view(), name='main_page'),
    url(r'^sign/$', views.SignPostView.as_view(), name='sign_post'),
    url(r'^mail$', views.MailView.as_view(), name='mail'),
    url(r'^edit/$', views.EditFormView.as_view(), name='edit_message'),
    url(r'^delete/$', views.DeleteFormView.as_view(), name='delete_message'),
    # url(r'^api/guestbook/(?P<guestbook_name>.+)/greeting/$', csrf_exempt(api.APIGreeting.as_view()), name='list_greeting'),
    # url(r'^api/guestbook/(?P<guestbook_name>.+)/greeting/(?P<id>(.)+)$', csrf_exempt(api.APIGreetingDetail.as_view()), name='item_greeting'),
    url(r'^api/guestbook/(?P<guestbook_name>.+)/greeting/$', api.APIGreeting.as_view(), name='list_greeting'),
    url(r'^api/guestbook/(?P<guestbook_name>.+)/greeting/(?P<id>(.)+)$', api.APIGreetingDetail.as_view(), name='item_greeting'),
]

