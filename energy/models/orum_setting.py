# coding: utf8
from django.db import models
from orum import Orum
from period import Period

__author__ = 'Demyanov Kirill'


class OrumSetting(models.Model):
    orum = models.ForeignKey(Orum)
    power = models.DecimalField(u'Установленная мощность',
                                decimal_places=5,
                                max_digits=14,
                                null=True,
                                )
    hours = models.PositiveIntegerField(u'Часы использования',
                                        default=1,
                                        null=True,
                                        blank=True
                                        )
    ratio = models.DecimalField(u'Коэффицент потребления',
                                decimal_places=6,
                                max_digits=8,
                                default=1,
                                null=True,
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

    def is_working_in(self, period):
        return period.between(self.installation_orum, self.removed_orum)

    def __str__(self):
        return u'%s' % self.id

    def __unicode__(self):
        return u"%s" % self.__str__()
