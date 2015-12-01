# coding: utf8
from django.db import models
from orum import Orum
from period import Period

__author__ = 'Demyanov Kirill'


class OrumDateUse(models.Model):
    orum = models.ForeignKey(Orum)
    period = models.ForeignKey(Period)
    date_use = models.PositiveIntegerField(u'Дней')

    class Meta:
        unique_together = ('orum', 'period')
