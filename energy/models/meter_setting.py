# coding: utf8
from django.db import models
from meter import Meter
from transformator import Transformer
from wire import Wire
from period import Period

__author__ = 'Demyanov Kirill'


class MeterSetting(models.Model):
    type_of_energy_choice = {
        (0, 'Активный'),
        (1, 'Реактивный'),
    }
    direction_energy_choice = {
        (0, 'Возврат в сеть'),
        (1, 'Отпуск в сеть'),
    }
    meter_place_choice = {
        (0, 'на границе'),
        (1, 'до границе'),
        (2, 'за границей'),
    }

    meter = models.ForeignKey(Meter)
    work_hours = models.PositiveSmallIntegerField(u'Количество часов работы')
    type_of_energy = models.PositiveSmallIntegerField(u'Вид энергии', choices=type_of_energy_choice)
    direction_energy = models.PositiveSmallIntegerField(u'Направление энергии', choices=direction_energy_choice)
    meter_place = models.PositiveSmallIntegerField(u'Место установки счетчика', choices=meter_place_choice)
    is_control = models.BooleanField(u'Контрольный счетчик')
    c_trans = models.DecimalField(u'Коэффициентр трансформации',
                                  decimal_places=4,
                                  max_digits=12,
                                  default=1,
                                  )
    c_loss = models.DecimalField(u'Коэффициентр потерь',
                                 decimal_places=4,
                                 max_digits=12,
                                 default=1,
                                 )
    transformer_loss = models.DecimalField(u'Потери в трансформаторе',
                                           decimal_places=4,
                                           max_digits=12,
                                           default=1,
                                           )
    cosfi = models.DecimalField(u'Коэффициентр трансформации',
                                decimal_places=5,
                                max_digits=9,
                                null=True,
                                blank=True,
                                )
    tangfi = models.DecimalField(u'Коэффициентр трансформации',
                                 decimal_places=5,
                                 max_digits=9,
                                 null=True,
                                 blank=True,
                                 )
    wire_length = models.DecimalField(u'Длина провода, в км',
                                      decimal_places=3,
                                      max_digits=6,
                                      null=True,
                                      blank=True,
                                      )
    wire_voltage = models.DecimalField(u'Напряжение линии, в кВ',
                                       decimal_places=2,
                                       max_digits=5,
                                       null=True,
                                       blank=True,
                                       )
    transformer = models.ForeignKey(Transformer)
    wire = models.ForeignKey(Wire)
    installation_meter = models.ForeignKey(Period,
                                           related_name='installation_meter_set',
                                           null=True,
                                           )
    removed_meter = models.ForeignKey(Period,
                                      related_name='removed_meter_set',
                                      null=True,
                                      blank=True,
                                      )