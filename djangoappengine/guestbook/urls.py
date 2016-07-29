from django.conf.urls import *
from guestbook.views import main_page, sign_post
from . import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'Django_StandAlone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', views.main_page, name='main_page'),
    url(r'^sign/$', views.sign_post, name='sign_post'),
]

