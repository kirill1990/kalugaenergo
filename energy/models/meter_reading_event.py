# coding: utf8
from django.db import models

__author__ = 'Demyanov Kirill'


class MeterReadingEvent(models.Model):
    title = models.CharField(u'Наименование', max_length=32)
    priority = models.PositiveSmallIntegerField(u'Приоритет показаний', unique=True)

    def __str__(self):
        return u'%s' % self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
