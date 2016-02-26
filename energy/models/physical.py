# coding: utf8
from django.core.urlresolvers import reverse
from django.db import models
from consumer import Consumer

__author__ = 'Demyanov Kirill'


class Physical(Consumer):

    class Meta:
        verbose_name = u'Физическое лицо'
        verbose_name_plural = u'Физическое лицо'

    seasonal_residence = models.BooleanField(
        verbose_name=u'Сезонное проживание',
    )

    def test(self):
        self.points
