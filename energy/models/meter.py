# coding: utf8
from django.db import models
from django.db.models import Sum
from decimal import Decimal
from meter_passport import MeterPassport
from power_grid_region import PowerGridRegion
from period import Period
# from meter_reading import MeterReading

__author__ = 'Demyanov Kirill'


class Meter(models.Model):
    serial_number = models.CharField(u'Номер счетчика',
                                     max_length=32,
                                     null=True,
                                     blank=True)

    passport = models.ForeignKey(MeterPassport)
    power_grid_region = models.ForeignKey(PowerGridRegion)

    date_created = models.DateField(u'Дата изготовления',
                                    null=True,
                                    blank=True)
    date_checked = models.DateField(u'Дата проверки',
                                    null=True,
                                    blank=True)

    last_date_instrumental = models.DateField(u'Дата последней инструментальной проверки',
                                              null=True,
                                              blank=True)
    next_date_instrumental = models.DateField(u'Дата следующей инструментальной проверки',
                                              null=True,
                                              blank=True)

    comment = models.TextField(u'Комментарий',
                               max_length=128,
                               null=True,
                               blank=True)

    def test(self):
        pass
        # period = Period.objects.get(pk=5)

    def get_reading_for(self, period):
        """
        Предоставляет показание для расчета за указанный период

        Для понимание, по каким критерием выбирается показание.
        период * is_true * приоритет *  показание
        4      * 1       *    4      *  133
        4      * 0       *    3      *  135
        4      * 0       *    4      *  137
        4      * 0       *    4      *  134
        4      * 0       *    4      *  131
        4      * 0       *    5      *  136
        3      * 0       *    3      *  120
        3      * 0       *    4      *  110
        3      * 0       *    5      *  125
        2      * 0       *    1      *  100
        В данном случ. выбирается число 133

        :param period: период, за который необходимо получить показание
        :return: показание за указанный период
        """

        # исключаются показания за ранние периоды, чем необходимо
        m_reading = self.meterreading_set.filter(period__lte=period)

        # исключаются события показаний установки и снятия счетчика
        m_reading = m_reading.exclude(event__in=[1, 2])

        # выставление показаний по приоритетным полям (см. таблицу)
        m_reading = m_reading.order_by('-period', '-is_true', 'event__priority', '-reading').first()

        return m_reading.reading if m_reading else self.meterreading_set.filter(event=1).first().reading

    def get_last_reading_for(self, period):
        """
        Предоставляет показание для расчета за прошлый период, указанного периода

        :param period: период, от которого расчитывается прошлый период
        :return: показание за прошлый период
        """
        return self.get_reading_for(period.last_period)

    def get_correction_in(self, period):
        """
        Предоставляет суммы корректировки kwh за указанный период

        :param period: период, за который необходимо получить корректировку
        :return: kwh корректировки
        """
        correction = self.metercorrection_set.filter(period=period).aggregate(Sum('kwh'))['kwh__sum']
        return round(correction, 3) if correction else Decimal(0)
