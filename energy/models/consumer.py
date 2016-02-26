# coding: utf8
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from production_area import ProductionArea
from point import Point
from time import Time

__author__ = 'Demyanov Kirill'


class Consumer(Time):

    class Meta:
        abstract = True

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
    title = models.CharField(
        u'Наименование потребителя',
        max_length=160,
    )
    points = GenericRelation(
        Point,
    )
    inn = models.CharField(
        u'ИНН',
        max_length=20,
        blank=True,
    )
    # points = models.ManyToManyField(
    #     Point,
    #     related_name="%(app_label)s_%(class)s_related",
    # )

    def __str__(self):
        return '%s: %s' % (self.ls, self.title)

    def __unicode__(self):
        return u"%s" % self.__str__()

    def current_period(self):
        return self.production_area.current_period
