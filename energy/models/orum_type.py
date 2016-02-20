# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models


class OrumType(models.Model):
    FORMULA_CHOICE = {
        (1, 'Постоянный расход'),
        (2, 'Расход * Количество дней'),
        (3, 'Расход * Количество дней * Часы'),
    }

    title = models.CharField('Наименование', max_length=31)
    formula = models.IntegerField('Формула', choices=FORMULA_CHOICE)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
