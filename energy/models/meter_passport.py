# coding: utf8
from django.db import models

__author__ = 'Demyanov Kirill'


class MeterPassport(models.Model):
    accuracy_class_choice = {
        (0, 'фиктивный'),
        (1, '2.5 и больше'),
        (2, '2.0'),
        (3, '1.5'),
        (4, '1.0'),
        (5, '0.5'),
        (6, '0.5S'),
        (7, '0.2'),
        (8, '0.2S'),
    }
    type_of_energy_choice = {
        (0, 'Активный'),
        (1, 'Реактивный'),
        (2, 'Активно-реактивный'),
    }
    type_of_meter_choice = {
        (0, 'Индукционный'),
        (1, 'Электронный'),
    }
    direct_choice = {
        (1, 'Однонаправленный'),
        (2, 'Двунаправленный'),
    }
    phase_choice = {
        (0, 'Однофазный'),
        (1, 'Трехфазный'),
    }
    tariff_choice = {
        (0, 'Однотарифный'),
        (1, 'Многотарифный(Зональный)'),
    }

    title = models.CharField(
        u'Наименование счетчика',
        max_length=64,
    )
    old_id = models.PositiveIntegerField(
        u'Старый id',
        null=True,
        db_index=True,
    )

    check = models.BooleanField(
        u'Проверенный',
    )
    active = models.BooleanField(
        u'Активный',
        default=True,
    )

    digits = models.PositiveSmallIntegerField(
        u'Целая часть',
    )
    decimals = models.PositiveSmallIntegerField(
        u'Дробная часть',
    )

    accuracy_class = models.PositiveSmallIntegerField(
        u'Класс точности',
        choices=accuracy_class_choice,
    )

    check_period = models.PositiveSmallIntegerField(
        u'Период проверки',
        null=True,
        blank=True,
    )
    replace_period = models.PositiveSmallIntegerField(
        u'Период замены',
        null=True,
        blank=True,
    )

    voltage = models.CharField(
        u'Напряжение',
        max_length=64,
        null=True,
        blank=True,
    )
    amperage = models.CharField(
        u'Ток',
        max_length=64,
        null=True,
        blank=True,
    )

    type_of_energy = models.PositiveSmallIntegerField(
        u'Вид энергии',
        choices=type_of_energy_choice,
    )
    type_of_meter = models.PositiveSmallIntegerField(
        u'Тип счетчика',
        choices=type_of_meter_choice,
    )

    tariff = models.PositiveSmallIntegerField(
        u'Тарифность',
        choices=tariff_choice,
    )
    phase = models.PositiveSmallIntegerField(
        u'Фаза',
        choices=phase_choice,
    )
    direct = models.PositiveSmallIntegerField(
        u'Направление',
        choices=direct_choice,
    )

    comment = models.TextField(
        u'Комментарий',
        max_length=182,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()
