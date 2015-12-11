# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models


class Period(models.Model):
    title = models.CharField('Наименование периода', max_length=30)
    date_start = models.DateField('Дата начала периода')
    last_period = models.ForeignKey('self', blank=True, null=True)
    faza_id = models.IntegerField('ID периодов в фазе', help_text='Шаблон yyyymm(201501)')

    def get_hour(self):
        """ Количество часов в периоде """
        if self.date_start.month in [1, 3, 5, 7, 8, 10, 12]:
            return 744
        elif self.date_start.month in [4, 6, 9, 11]:
            return 720
        elif self.date_start.month in [2]:
            return 696 if self.date_start.year % 4 == 0 else 672

    def is_between(self, left, right):
        """
        Проверяет нахождения периода внутри временной линии между двумя другими
        :param left: период до
        :param right: период после(возможен None)
        :return: True - период входит в промежуток
                 False - период не входит в промежуток
        """
        return True if left.date_start <= self.date_start and \
                       (not right or self.date_start < right.date_start) else False

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
