# coding: utf8
from django.db import models
from point import Point
from meter import Meter
from orum import Orum
from period import Period

__author__ = 'Demyanov Kirill'

class PointMeter(models.Model):
    point = models.ForeignKey(
        Point
    )
    meter = models.ForeignKey(
        Meter,
        null=True,
        blank=True,
    )
    installation_in_period = models.ForeignKey(
        Period,
        related_name='installation_point_meter_set',
    )
    removed_in_period = models.ForeignKey(
        Period,
        related_name='removed_point_meter_set',
        null=True,
        blank=True,
    )
