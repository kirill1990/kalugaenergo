# coding: utf8
from decimal import Decimal
from django.db import models
from django.db.models import Sum
from orum_type import OrumType
from period import Period

__author__ = 'Demyanov Kirill'


class Orum(models.Model):
    type = models.ForeignKey(OrumType)

    def get_setting_in(self, period):
        """
        Получение setting за указанный период

        :param period: Период, за который необходимо получить setting
        :return: setting выбранного периода
                 None - setting не найден
        """
        settings = [element for element in self.orumsetting_set.all() if element.is_working_in(period)]
        return settings[0] if settings.__len__() > 0 else None

    def get_correction_in(self, period):
        """
        Получение суммы корректировки kwh за указанный период

        :param period: Период, за который необходимо получить корректировку
        :return: kwh корректировки
        """
        correction = self.orumcorrection_set.filter(period=period).aggregate(Sum('kwh'))['kwh__sum']
        return correction if correction else Decimal(0)

    def get_date_use(self, period):
        """
        Получение date_use за указанный период

        :param period: Период, за который необходимо получить date_use
        :return: date_use выбранного периода
                 None - date_use не найден
        """
        model_du = self.orumdateuse_set.filter(period=period).first()
        return model_du.date_use if model_du else None

    def value(self, period=Period.objects.get(pk=6)):
        """ description """

        setting = self.get_setting_in(period)
        date_use = self.get_date_use(period)

        if not setting or not date_use and self.type.formula in (2, 3):
            return None

        result = setting.ratio * setting.power

        if self.type.formula in (2, 3):
            result *= date_use

            if self.type.formula == 3:
                result *= setting.hours

        correction = self.get_correction_in(period)

        return round(Decimal(result) + correction, 3)

    def __str__(self):
        return u'%s: %i' % (self.type.title, self.pk)

    def __unicode__(self):
        return u"%s" % self.__str__()
