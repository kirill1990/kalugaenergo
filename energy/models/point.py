# coding: utf8
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
# from energy.models.consumer import Consumer
# from energy.models.point_meter_orum import MeterOrum

__author__ = 'Demyanov Kirill'

class Point(models.Model):
    number_in_t2 = models.PositiveIntegerField(
        u'Уникальный номер из т2',
        unique=True,
        blank=True,
        null=True,
    )
    title = models.CharField(
        u'Наименование точки учета',
        max_length=100
    )

    content_type = models.ForeignKey(
        ContentType,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u"%s" % self.__str__()

    def get_work_meter(self, period):
        meter = self.pointmeter_set.filter(
            Q(installation_in_period__lte=period)
            & (
                Q(removed_in_period__isnull=True)
                | Q(removed_in_period__gt=period)
            )
        )

        return meter.first().meter

    def get_work_orum(self, period):
        orum = self.orum_set.filter(
            Q(installation_in_period__lte=period)
            & (
                Q(removed_in_period__isnull=True)
                | Q(removed_in_period__gt=period)
            )
        )
        return orum.first()

    def orum_in_current_period(self):
        period = self.consumer.production_area.power_grid_region.current_period
        orum = self.get_work_orum(period)
        if orum:
            orum = orum.orum
            setting = orum.get_setting_in(period)
            value = orum.get_kwh_in(period)
            correction = orum.get_correction_in(period)
            date_use = orum.get_date_use(period)
            date_use = '' if date_use is None else date_use
            return dict(point=self, orum=orum, setting=setting, value=value, correction=correction, date_use=date_use)
        return None

    def value(self):
        pass

    def value_in_current_period(self):

        period = self.consumer.production_area.power_grid_region.current_period
        orum = self.get_work_orum(period)

        if orum:
            return orum.orum.get_kwh_in(period)

        # if self.orum:
        #     return self.orum.filter()
        # if self.meter:
        #     return 0
        return 0
