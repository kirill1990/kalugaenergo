# coding: utf8
from django.test import TestCase
from energy.models import Orum, OrumType, Period, OrumDateUse, OrumSetting, OrumCorrection, Point

__author__ = 'Demyanov Kirill'

class TestOrumSetting(TestCase):
    fixtures = ['energy_fixtures']

    def setUp(self):
        self.types = {OrumType.objects.get(pk=x).formula: OrumType.objects.get(pk=x) for x in range(6, 9)}
        self.periods = {x: Period.objects.get(pk=x) for x in range(1, 11)}
        self.point = Point.objects.create(title='')

    def test_valid_orum_type(self):
        """ Для орумов предусмотрено 8 типов """

        self.assertEqual(OrumType.objects.all().count(), 8)

    def test_hours_default_equal_1(self):
        """ В орумах часы использования по умолчанию 1 """

        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])
        setting = OrumSetting.objects.create(type=self.types[1], orum=orum, power=3, ratio=1, installation_orum=self.periods[2])
        self.assertEqual(setting.hours, 1)

    def test_ratio_default_equal_1(self):
        """ В орумах коэффициент по умолчанию 1 """
        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])
        setting = OrumSetting.objects.create(type=self.types[1], orum=orum, power=3, installation_orum=self.periods[2])
        self.assertEqual(setting.ratio, 1)
