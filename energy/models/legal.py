# coding: utf8
from django.core.urlresolvers import reverse
from django.db import models
from consumer import Consumer

__author__ = 'Demyanov Kirill'


class Legal(Consumer):

    class Meta:
        verbose_name = u'Юридическое лицо'
        verbose_name_plural = u'Юридическое лицо'

    kpp = models.CharField(
        u'КПП',
        max_length=20,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse('energy:consumer', kwargs={'pk': self.id})
