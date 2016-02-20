__author__ = 'Demyanov Kirill'

from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^consumer$', views.Consumers.as_view(), name='consumers'),
    url(r'^consumer/add$', views.ConsumerCreate.as_view(), name='consumer_add'),

    url(r'^consumer/(?P<pk>[0-9]+)$', views.ConsumerDetail.as_view(), name='consumer'),

    # url(r'^consumer/(?P<pk>[0-9]+)/points$', views.MeterList.as_view(), name='consumer_meter_list'),

    url(r'^consumer/(?P<pk>[0-9]+)/meter$', views.MeterList.as_view(), name='consumer_meters'),
    url(r'^consumer/meter/refresh$', views.MeterRefresh.as_view(), name='meter_refresh'),

    url(r'^consumer/(?P<pk>[0-9]+)/orum$', views.ConsumerOrums.as_view(), name='consumer_orums'),
    url(r'^consumer/orum/update/date_use$', views.OrumUpdateDateUse.as_view(), name='orum_update_date_use'),
    url(r'^consumer/orum/refresh$', views.OrumRefresh.as_view(), name='orum_refresh'),

    url(r'^consumer/(?P<pk>[0-9]+)/orum/add$', views.OrumAdd.as_view(), name='orum_add'),

    url(r'^orum/(?P<pk>[0-9]+)/setting$', views.OrumDetail.as_view(), name='orum_setting'),

    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
]
