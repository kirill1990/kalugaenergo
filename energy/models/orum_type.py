# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models


class OrumType(models.Model):
    FORMULA_CHOICE = {
        (1, u'Постоянный расход'),
        (2, u'Расход * Количество дней'),
        (3, u'Расход * Количество дней * Часы'),
    }

    title = models.CharField(u'Наименование', max_length=31)
    formula = models.IntegerField(u'Формула', choices=FORMULA_CHOICE)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
