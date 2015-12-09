# coding: utf8
from django.db import models

__author__ = 'Demyanov Kirill'


class Transformer(models.Model):
    old_id = models.PositiveIntegerField(u'Уникальный номер из т2')
    title = models.CharField(u'Наименование трансформатора', max_length=64)
    pxx = models.DecimalField(u'Потери холостого хода',
                              decimal_places=4,
                              max_digits=14,
                              )
    pkz = models.DecimalField(u'Потери в обмотках',
                              decimal_places=4,
                              max_digits=14,
                              )
    s = models.PositiveIntegerField(u'Номинальная мощность трансформатора, кВа')
    comment = models.TextField(u'Комментарий', max_length=128, null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
