# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models
from orum import Orum
from period import Period


class OrumValue(models.Model):
    orum = models.ForeignKey(Orum)
    period = models.ForeignKey(Period)
    date_use = models.PositiveIntegerField(u'Дней', default=1)
    kwh = models.DecimalField(u'Добавка',
                              decimal_places=5,
                              max_digits=17,
                              default=0
                              )

    class Meta:
        unique_together = ('orum', 'period')

    def __str__(self):
            return u'Запись за %s, орума %s' % (self.period.title, self.orum)

    def __unicode__(self):
        return u"%s" % self.__str__()
