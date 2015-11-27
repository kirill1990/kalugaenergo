# coding: utf8

__author__ = 'Demyanov Kirill'

from django.db import models


class Meter(models.Model):
    serial_number = models.CharField('Номер счетчика', max_length=20, null=True)


    def test(self):
        pass
        # self.point_set.