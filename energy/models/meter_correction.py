# coding: utf8
from django.db import models
from meter import Meter
from period import Period

__author__ = 'Demyanov Kirill'


class MeterCorrection(models.Model):
    meter = models.ForeignKey(
        Meter,
    )
    period = models.ForeignKey(
        Period,
    )
    kwh = models.DecimalField(
        u'Корректировка в kwh',
        decimal_places=5,
        max_digits=17,
        default=0,
    )
