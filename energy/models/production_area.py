# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models
from period import Period


class ProductionArea(models.Model):
    title = models.CharField(
        u'Наименование участка',
        max_length=20,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
    )
    current_period = models.ForeignKey(
        Period,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
