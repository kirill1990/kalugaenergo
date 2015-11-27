# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models
from network_organization import NetworkOrganization

class ProductionDepartment(models.Model):
    title = models.CharField(u'Наименвоание производственного отеделения', max_length=64)
    network_organization = models.ForeignKey(NetworkOrganization)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
