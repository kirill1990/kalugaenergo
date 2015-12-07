# coding: utf8
from django.db import models

__author__ = 'Demyanov Kirill'


class Wire(models.Model):
    old_id = models.PositiveIntegerField(u'Уникальный номер из т2')
    title = models.CharField(u'Наименование провода', max_length=64)
    ro = models.DecimalField(u'Удельное сопротивление провода',
                             decimal_places=4,
                             max_digits=7,
                             )
    comment = models.TextField(u'Комментарий', max_length=128, null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
