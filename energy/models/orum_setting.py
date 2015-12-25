# coding: utf8
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from orum import Orum
from period import Period

__author__ = 'Demyanov Kirill'


class OrumSetting(models.Model):
    orum = models.ForeignKey(Orum)
    power = models.DecimalField(u'Установленная мощность',
                                decimal_places=5,
                                max_digits=14,
                                null=True,
                                validators=[MinValueValidator(0.0001), MaxValueValidator(1000000)],
                                )
    hours = models.PositiveIntegerField(u'Часы использования',
                                        default=1,
                                        null=True,
                                        blank=True,
                                        validators=[MinValueValidator(0), MaxValueValidator(1000)],
                                        )
    ratio = models.DecimalField(u'Коэффицент потребления',
                                decimal_places=6,
                                max_digits=8,
                                default=1,
                                null=True,
                                validators=[MinValueValidator(0), MaxValueValidator(1000)],
                                )
    installation_orum = models.ForeignKey(Period,
                                          related_name='installation_orum_set',
                                          null=True,
                                          )
    removed_orum = models.ForeignKey(Period,
                                     related_name='removed_orum_set',
                                     null=True,
                                     blank=True,
                                     )

    def __str__(self):
        return u'%s' % self.id

    def __unicode__(self):
        return u"%s" % self.__str__()
