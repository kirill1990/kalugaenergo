# coding: utf8
from decimal import Decimal
from django.db import models
from django.db.models import Q
from django.db.models import Sum
from point import Point
from period import Period

__author__ = 'Demyanov Kirill'


class Orum(models.Model):
    point = models.ForeignKey(
        Point
    )
    installation_in_period = models.ForeignKey(
        Period,
        related_name='installation_in_period_set',
    )
    removed_in_period = models.ForeignKey(
        Period,
        related_name='removed_in_period_set',
        null=True,
        blank=True,
    )

    def get_setting_in(self, period):
        """
        Предоставляет setting за указанный период

        :param period: период, за который необходимо получить setting
        :return: setting выбранного периода
                 None - setting не найден
        """
        settings = self.orumsetting_set.filter(
            Q(installation_orum__lte=period, removed_orum__gt=period)
            | Q(installation_orum__lte=period, removed_orum__isnull=True)
        )
        return settings.first()

    def get_correction_in(self, period):
        """
        Предоставляет суммы корректировки kwh за указанный период

        :param period: период, за который необходимо получить корректировку
        :return: kwh корректировки
        """
        correction = self.orumcorrection_set.filter(period=period).aggregate(Sum('kwh'))['kwh__sum']
        return Decimal(round(correction, 3)) if correction else Decimal(0)

    def get_date_use(self, period):
        """
        Предоставляет date_use за указанный период

        :param period: период, за который необходимо получить date_use
        :return: date_use выбранного периода
                 None - date_use не найден
        """
        model_du = self.orumdateuse_set.filter(period=period).first()
        return model_du.date_use if model_du else None

    def get_kwh_in(self, period):
        """
        Предоставляет потребление в kwh за указанный период

        формула 1:
            kwh = [Мощность]
                    * [Коэффициент]
                    + [Корректировка в kwh]
        формула 2:
            kwh = [Мощность]
                    * [Количество дней в использование]
                    * [Коэффициент]
                    + [Корректировка в kwh]
        формула 3:
            kwh = [Мощность]
                    * [Количество дней в использование]
                    * [Время использования в день]
                    * [Коэффициент]
                    + [Корректировка в kwh]

        :param period: период, за который необходимо получить потребление
        :return: потребление в kwh за выбранный период
        """

        setting = self.get_setting_in(period)
        date_use = self.get_date_use(period)

        if not setting or not date_use and setting.type.formula in (2, 3):
            return None

        kwh = setting.ratio * setting.power

        if setting.type.formula in (2, 3):
            kwh *= date_use

            if setting.type.formula == 3:
                kwh *= setting.hours

        correction = self.get_correction_in(period)

        return round(Decimal(kwh) + correction, 3)

    def __str__(self):
        return u'%s: %i' % (self.point, self.pk)

    def __unicode__(self):
        return u"%s" % self.__str__()
