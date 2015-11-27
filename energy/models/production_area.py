# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models
from power_grid_region import PowerGridRegion


class ProductionArea(models.Model):
    title = models.CharField('Наименование участка', max_length=20)
    power_grid_region = models.ForeignKey(PowerGridRegion)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
