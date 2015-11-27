# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models

class NetworkOrganization(models.Model):
    title = models.CharField(u'Наименвоание сетевой организации', max_length=64)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
