# coding: utf8
from django.db import models
from energy.models.period import Period
from energy.models.meter import Meter
from energy.models.meter_reading_event import MeterReadingEvent

__author__ = 'Demyanov Kirill'


class MeterReading(models.Model):
    meter = models.ForeignKey(Meter)
    period = models.ForeignKey(Period)
    event = models.ForeignKey(MeterReadingEvent)
    is_true = models.BooleanField(u'Принимать показание',
                                  default=False
                                  )
    reading = models.DecimalField(u'Показание счетчика',
                                  decimal_places=5,
                                  max_digits=17,
                                  default=0
                                  )

    def __str__(self):
        return self.reading

    def __unicode__(self):
        return u"%s" % self.__str__()
