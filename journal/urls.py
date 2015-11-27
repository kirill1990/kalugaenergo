__author__ = 'Demyanov Kirill'

from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'message/add/$', views.get_name, name='message_add'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]