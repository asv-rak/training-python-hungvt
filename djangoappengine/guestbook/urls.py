from django.conf.urls import *
from . import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'Django_StandAlone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', views.MainPage.as_view(), name='main_page'),
    url(r'^sign/$', views.SignPost.as_view(), name='sign_post'),
]

