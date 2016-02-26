from django.contrib.auth.decorators import login_required

__author__ = 'Demyanov Kirill'

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^legal$', views.Legals.as_view(), name='legals'),
    url(r'^legal/add$', views.ConsumerCreate.as_view(), name='legal_add'),

    url(r'^legal/(?P<pk>[0-9]+)/detail$', views.LegalDetail.as_view(), name='legal_detail'),

    url(r'^consumer/(?P<pk>[0-9]+)/points$', views.MeterList.as_view(), name='consumer_meter_list'),

    url(r'^legal/(?P<pk>[0-9]+)/meter$', views.MeterList.as_view(), name='legal_meters'),
    url(r'^legal/meter/refresh$', views.MeterRefresh.as_view(), name='meter_refresh'),

    url(r'^legal/(?P<pk>[0-9]+)/orum$', views.ConsumerOrums.as_view(), name='legal_orums'),
    url(r'^legal/orum/update/date_use$', views.OrumUpdateDateUse.as_view(), name='orum_update_date_use'),
    url(r'^legal/orum/refresh$', views.OrumRefresh.as_view(), name='orum_refresh'),

    url(r'^legal/(?P<pk>[0-9]+)/orum/add$', views.OrumAdd.as_view(), name='orum_add'),

    url(r'^orum/(?P<pk>[0-9]+)/setting$', views.OrumDetail.as_view(), name='orum_setting'),
]
