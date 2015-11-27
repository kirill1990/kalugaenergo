# coding: utf8
__author__ = 'Demyanov Kirill'

from django.db import models


class ConsumerType(models.Model):
    name = models.CharField('Тип потребителя', max_length=35)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.__str__()
