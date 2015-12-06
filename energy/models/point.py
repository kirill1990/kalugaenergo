# coding: utf8
from django.db import models
from consumer import Consumer
from meter import Meter
from orum import Orum

__author__ = 'Demyanov Kirill'

class Point(models.Model):
    name = models.CharField('Наименование точки учета', max_length=100)
    consumer = models.ForeignKey(Consumer, null=True)
    # meter = models.ManyToManyField(Meter,
    #                                blank=True,
    #                                through=)
    orum = models.ManyToManyField(Orum,
                                  through='MeterOrum',
                                  through_fields=('point', 'orum')
                                  )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % self.__str__()

    def value(self):
        period = self.consumer.production_area.power_grid_region.current_period
        self.orum
        # if self.orum:
        #     return self.orum.filter()
        # if self.meter:
        #     return 0
        return 0
