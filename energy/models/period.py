# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models


class Period(models.Model):
    title = models.CharField('Наименование периода', max_length=30)
    date_start = models.DateField('Дата начала периода')
    last_period = models.ForeignKey('self', blank=True, null=True)
    faza_id = models.IntegerField('ID периодов в фазе', help_text='Шаблон yyyymm(201501)')

    def between(self, left, right):
        if left.date_start <= self.date_start and (not right or self.date_start < right.date_start):
            return True

        return False

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
