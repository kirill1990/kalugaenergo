# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models
from consumer_type import ConsumerType
from production_area import ProductionArea


class Consumer(models.Model):
    ls = models.CharField('Лицевой счет', max_length=10)
    name = models.CharField('Наименование потребителя', max_length=150)
    type = models.ForeignKey(ConsumerType)
    production_area = models.ForeignKey(ProductionArea, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.__str__()
