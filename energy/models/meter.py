# coding: utf8
import math
from django.db import models
from django.db.models import Sum
from decimal import Decimal
from meter_passport import MeterPassport
from power_grid_region import PowerGridRegion
# from period import Period
# from meter_reading import MeterReading

__author__ = 'Demyanov Kirill'


class Meter(models.Model):
    serial_number = models.CharField(
        u'Номер счетчика',
        max_length=32,
        null=True,
        blank=True,
    )
    passport = models.ForeignKey(
        MeterPassport,
    )
    power_grid_region = models.ForeignKey(
        PowerGridRegion,
    )
    date_created = models.DateField(
        u'Дата изготовления',
        null=True,
        blank=True,
    )
    date_checked = models.DateField(
        u'Дата проверки',
        null=True,
        blank=True,
    )
    last_date_instrumental = models.DateField(
        u'Дата последней инструментальной проверки',
        null=True,
        blank=True
    )
    next_date_instrumental = models.DateField(
        u'Дата следующей инструментальной проверки',
        null=True,
        blank=True,
    )
    comment = models.TextField(
        u'Комментарий',
        max_length=128,
        null=True,
        blank=True,
    )

    def test(self):
        pass
        # period = Period.objects.get(pk=5)

    def reading(self, period, status):
        """
        Показание на указанный период

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

        * is_true - Принимать показание
        """

        if status:
            # исключаются показания за ранние периоды, чем необходимо
            m_reading = self.meterreading_set.filter(period__lte=period)
        else:
            # показание за ранние периоды, чем необходимо
            m_reading = self.meterreading_set.filter(period=period)

        # исключаются события показаний установки и снятия счетчика
        m_reading = m_reading.exclude(event__in=[1, 2])

        # выставление показаний по приоритетным полям (см. таблицу)
        m_reading = m_reading.order_by('-period', '-is_true', 'event__priority', '-reading').first()

        if m_reading:
            return m_reading.reading
        else:
            return self.meterreading_set.filter(event=1).first().reading if status else None

    def reading_in(self, period):
        """ Показание в указанный период """
        return self.reading(period=period, status=False)

    def reading_for(self, period):
        """ Показание на указанный период """
        return self.reading(period=period, status=True)

    def last_reading_for(self, period):
        """ Показание за прошлый период, от указанного периода """

        return self.reading_for(period.last_period)

    def correction_in(self, period):
        """ Сумма корректировки kwh за указанный период"""

        correction = self.metercorrection_set.filter(period=period).aggregate(Sum('kwh'))['kwh__sum']
        return Decimal(round(correction, 3)) if correction else Decimal(0)

    def kwh_consumption(self, period):
        """ kwh с учетом коэффициентов потребления и потерь за период по счетчику """

        setting = self.setting_in(period)
        return Decimal(round(self.kwh_meter(period) * setting.c_loss * setting.c_trans, 3))

    def kwh_meter(self, period):
        """ kwh за период по счетчику """

        current_reading = self.reading_for(period)
        last_reading = self.last_reading_for(period)

        # переход через ноль счетчика
        correct = 10**self.passport.digits if current_reading < last_reading else 0

        return Decimal(current_reading - last_reading + correct)

    def kwh(self, period):
        """ kwh - полное потребление за период с учетом коэффицинтов и всех потерь """

        setting = self.setting_in(period)

        if setting:
            consumption = self.kwh_consumption(period)
            correction = self.correction_in(period)

            wire_loss = self.loss_in_wire(setting=setting, period=period)
            transformer_loss = self.loss_in_transformer(setting=setting, period=period)

            result = consumption + correction + wire_loss + transformer_loss
        else:
            return 0
        return Decimal(result)

    def setting_in(self, period):
        """ Параметры установки счетчика за указанный период """

        settings = [element for element in self.metersetting_set.all() if element.is_working_in(period)]
        return settings[0] if settings.__len__() > 0 else None

    def loss_in_transformer_period(self, period):
        setting = self.setting_in(period)
        return self.loss_in_transformer(period, setting)

    def loss_in_transformer(self, period, setting):
        """
        Потери в трансформаторе

        ΔWтхх = ΔPxx * Твкл
        ΔPxx - Потери холостого хода в сердечнике трансформатора
        Твкл - Число часов работы трансформатора в месяц(время включения), час(744,720,696,672)

        ΔWт = Wмес^2 * ΔPкз / (Траб * Sн^2 * cosφ^2)
        Wмес - Потребление энергии за месяц
        ΔPкз - Потери в обмотках при номинальной нагрузке трансформатора
        Траб - Число часов работы трансформатора в меся с нагрузкой за месяц
        Sн - Номинальная мощность трансформатора
        cosφ - Коэффициент мощности электрической энергии
        """
        if setting is None:
            setting = self.setting_in(period)

        if setting.transformer:
            consumption = self.kwh_consumption(period)
            pxx = setting.transformer.pxx
            pkz = setting.transformer.pkz
            s = setting.transformer.s
            hours = period.get_hour()
            work_h = setting.work_hours
            cosfi = self.cosfi(setting)

            if work_h is None:
                work_h = hours * s * cosfi / consumption

            # потери холостого хода в трансформаторе
            w_txx = pxx * hours

            # потери электроэнергии в рабочем трансформаторе
            w_t = consumption**2 * pkz / (Decimal(work_h) * s**2 * cosfi**2)

            return round((w_txx + w_t) * setting.transformer_loss, 3)
        return 0

    def loss_in_wire_period(self, period):
        setting = self.setting_in(period)
        return self.loss_in_wire(period, setting)

    def loss_in_wire(self, period, setting):
        """
        Потери в линии

        ΔWлин = Wмес^2 * ro * L / (1000 * Твкл * U^2 * cosφ^2)
        Wмес - Потребление энергии за месяц
        ro - Удельное сопротивление провода(кабеля)
        L - Длина линии электропереач(ЛЭП)
        Твкл - Число часов работы трансформатора в месяц(время включения), час(744,720,696,672)
        U - ЛИнейное напряжение
        cosφ - Коэффициент мощности электрической энергии
        """

        if setting is None:
            setting = self.setting_in(period)

        if setting.wire:
            ro = setting.wire.ro
            voltage = setting.wire_voltage
            length = setting.wire_length
            hours = period.get_hour()
            cosfi = self.cosfi(setting)

            consumption = self.kwh_consumption(period)

            result = consumption**2 * ro * length / (1000 * hours * (voltage * cosfi)**2)
            return Decimal(round(result, 3))
        return 0

    @staticmethod
    def cosfi(setting):
        """ Косинус фи """

        cosfi = 0.8
        if setting.cosfi:
            cosfi = setting.cosfi
        elif setting.tangfi:
            cosfi = 1 / math.sqrt(1 + setting.tangfi**2)
        return Decimal(round(cosfi, 9))

    def __str__(self):
        return '%s / %s' % (self.serial_number, self.passport.title)

    def __unicode__(self):
        return u"%s" % self.__str__()
