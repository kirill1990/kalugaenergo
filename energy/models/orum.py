# coding: utf8
from decimal import Decimal
from django.core.exceptions import ValidationError


__author__ = 'Demyanov Kirill'

from django.db import models
from orum_type import OrumType
from period import Period


def validate_even(value):
    if value <= 0:
        raise ValidationError(u'Ошибка: %s. Значение должно быть больше нуля' % value)

class Orum(models.Model):
    type = models.ForeignKey(OrumType)
    power = models.DecimalField(u'Установленная мощность',
                                decimal_places=5,
                                max_digits=14
                                )
    hours = models.PositiveIntegerField(u'Часы использования', default=1)
    ratio = models.DecimalField(u'Коэффицент потребления',
                                decimal_places=6,
                                max_digits=8,
                                validators=[validate_even],
                                default=1
                                )
    installation_in_period = models.ForeignKey(Period, related_name='installation_in_period')
    removed_in_period = models.ForeignKey(Period,
                                          related_name='removed_in_period',
                                          null=True,
                                          blank=True
                                          )

    def value(self, period):
        """ description """

        """ дата """
        if not period.between(self.installation_in_period, self.removed_in_period):
            return None

        """ вычисление """
        orum_value = self.orumvalue_set.filter(period=period).first()

        if not orum_value:
            orum_value = self.orumvalue_set.create(period=period)

        if orum_value:
            test = {
                1: self.power,
                2: self.power * orum_value.date_use,
                3: self.power * orum_value.date_use * self.hours,
            }.get(self.type.formula) * self.ratio

            return round(Decimal(test) + orum_value.kwh, 6)
        return 0

    def __str__(self):
        return u'%s %f/%d/%f' % (self.type.title, self.power, self.hours, self.ratio)

    def __unicode__(self):
        return u"%s" % self.__str__()
