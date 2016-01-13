# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models
from period import Period
from production_department import ProductionDepartment


class PowerGridRegion(models.Model):
    title = models.CharField('Наименование РЭСа', max_length=30)
    current_period = models.ForeignKey(Period)
    production_department = models.ForeignKey(ProductionDepartment, null=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
