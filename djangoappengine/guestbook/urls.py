from django.conf.urls import *

from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Django_StandAlone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', views.MainPageView.as_view(), name='main_page'),
    url(r'^sign/$', views.SignPostView.as_view(), name='sign_post'),
    url(r'^mail$', views.MailView.as_view(), name='mail'),
    url(r'^edit/$', views.EditFormView.as_view(), name='edit_message'),
    url(r'^delete/$', views.DeleteFormView.as_view(), name='delete_message'),
]

