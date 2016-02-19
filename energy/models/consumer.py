# coding: utf8
from django.core.urlresolvers import reverse
from django.db import models
from production_area import ProductionArea

__author__ = 'Demyanov Kirill'


class Consumer(models.Model):
    TYPE_CHOICE = {
        (0, 'Юридическое лицо'),
        (1, 'Бытовой потребитель'),
    }
    type = models.IntegerField(
        verbose_name=u'Тип потербителя',
        choices=TYPE_CHOICE,
        null=False,
    )
    production_area = models.ForeignKey(
        ProductionArea,
        verbose_name=u'Производственный участок',
        null=True,
    )
    old_id = models.PositiveIntegerField(
        u'Уникальный номер из т2',
        unique=True,
        blank=True,
        null=True,
    )
    ls = models.CharField(
        u'Лицевой счет',
        max_length=10,
    )
    name = models.CharField(
        u'Наименование потребителя',
        max_length=160,
    )
    inn = models.CharField(
        u'ИНН',
        max_length=20,
        blank=True,
    )
    kpp = models.CharField(
        u'КПП',
        max_length=20,
        blank=True,
    )

    def __str__(self):
        return '%s: %s' % (self.ls, self.name)

    def __unicode__(self):
        return u"%s" % self.__str__()
    
    def test(self):
        self.point_set.count()
        pass

    def current_period(self):
        return self.production_area.power_grid_region.current_period

    def get_absolute_url(self):
        return reverse('energy:consumer', kwargs={'pk': self.id})
