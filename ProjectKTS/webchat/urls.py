from django.urls import path
from django.conf.urls import include , url
from .import views

urlpatterns = [
    url(r'^auth/$', views.auth, name='auth'),
    url(r'^reg/$', views.reg, name='reg'),
    url(r'^$', views.index, name='chat'),
    url(r'^room$', views.room, name='room'),
    url(r'^mylogout$', views.mylogout, name='mylogout'),
    url(r'^create_chat/$', views.create_chat, name='create_chat'),
    url(r'^(?P<pk>\d+)$', views.open_chat, name='open_chat'),
    url(r'^(?P<pk>\d+)/send$', views.send_message, name='send_message'),
]