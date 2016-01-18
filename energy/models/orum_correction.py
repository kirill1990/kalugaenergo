# coding: utf8
from django.db import models
from orum import Orum
from period import Period

__author__ = 'Demyanov Kirill'


class OrumCorrection(models.Model):
    orum = models.ForeignKey(
        Orum
    )
    period = models.ForeignKey(
        Period,
        null=True
    )
    kwh = models.DecimalField(
        u'Корректировка в kwh',
        decimal_places=5,
        max_digits=17,
        default=0
    )
