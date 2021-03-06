# coding: utf8
from django.test import TestCase
from energy.models import Orum, OrumType, Period, OrumDateUse, OrumSetting, OrumCorrection, Point

__author__ = 'Demyanov Kirill'

class TestOrum(TestCase):
    fixtures = ['energy_fixtures']

    def setUp(self):
        self.types = {OrumType.objects.get(pk=x).formula: OrumType.objects.get(pk=x) for x in range(6, 9)}
        self.periods = {x: Period.objects.get(pk=x) for x in range(1, 11)}
        self.point = Point.objects.create(title='')

    def test_none_period(self):
        """ Запрос по периоду, в котором не было/нет орума """
        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])
        setting = OrumSetting(type=self.types[1], orum=orum, power=3, ratio=1, installation_orum=self.periods[2])
        setting.removed_orum = self.periods[5]
        setting.save()

        self.assertEqual(orum.get_kwh_in(self.periods[1]), None)
        self.assertEqual(orum.get_kwh_in(self.periods[5]), None)
        self.assertEqual(orum.get_kwh_in(self.periods[6]), None)

    def test_value_orum_formula_1(self):
        """
        Проверяет правильность вычисления потребления
        орумов по формуле 1:
            kwh = [Мощность]
                        * [Коэффициент]
                        + [Корректировка в kwh]
        """

        """ Задана только [Мощность] """
        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])
        setting = OrumSetting.objects.create(type=self.types[1], orum=orum, power=0.01, installation_orum=self.periods[1])
        self.assertEqual(setting.type.formula, 1)
        self.assertEqual(orum.get_kwh_in(self.periods[1]), 0.01)
        self.assertEqual(orum.get_kwh_in(self.periods[2]), 0.01)

        """ + [Коэффициент] """
        setting.ratio = 0.1
        setting.save()
        self.assertEqual(orum.get_kwh_in(self.periods[3]), 0.001)

        """ + [Корректировка в kwh] """
        OrumCorrection.objects.create(orum=orum, period=self.periods[4], kwh=1.34)
        self.assertEqual(orum.get_kwh_in(self.periods[4]), 1.341)

    def test_value_orum_formula_2(self):
        """
        Проверяет правильность вычисления потребления
        орумов по формуле 2:
            kwh = [Мощность]
                        * [Количество дней в использование]
                        * [Коэффициент]
                        + [Корректировка в kwh]
        """
        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])
        setting = OrumSetting.objects.create(type=self.types[2], orum=orum, power=0.01, installation_orum=self.periods[1])
        self.assertEqual(setting.type.formula, 2)

        """ Задана [Мощность] и [Количество дней в использование] """
        OrumDateUse.objects.create(orum=orum, period=self.periods[1], date_use=3)
        self.assertEqual(orum.get_kwh_in(self.periods[1]), 0.03)

        """ Задана [Мощность], [Количество дней в использование], [Корректировка в kwh] """
        OrumCorrection.objects.create(orum=orum, period=self.periods[1], kwh=3.23)
        self.assertEqual(orum.get_kwh_in(self.periods[1]), 3.26)

    def test_value_orum_formula_3(self):
        """
        Проверяет правильность вычисления потребления
        орумов по формуле 3:
            kwh = [Мощность]
                    * [Количество дней в использование]
                    * [Время использования в день]
                    * [Коэффициент]
                    + [Корректировка в kwh]
        """
        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])
        setting = OrumSetting.objects.create(type=self.types[3], orum=orum, power=0.01, installation_orum=self.periods[1], hours=2)
        self.assertEqual(setting.type.formula, 3)

        """ Задана [Мощность], [Количество дней в использование] """
        OrumDateUse.objects.create(orum=orum, period=self.periods[1], date_use=3)
        self.assertEqual(orum.get_kwh_in(self.periods[1]), 0.06)

        """ Задана [Мощность], [Количество дней в использование], [Корректировка в kwh] """
        OrumCorrection.objects.create(orum=orum, period=self.periods[1], kwh=3.23)
        self.assertEqual(orum.get_kwh_in(self.periods[1]), 3.29)

    def test_get_date_use(self):
        """
        Проверяет правильность получения объекта date_use
        """
        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])
        OrumDateUse.objects.create(orum=orum, period=self.periods[2], date_use=3)

        self.assertIsNotNone(orum.get_date_use(period=self.periods[2]))
        self.assertEqual(orum.get_date_use(period=self.periods[2]), 3)
        self.assertIsNone(orum.get_date_use(period=self.periods[3]))

    def test_get_setting_in(self):
        """
        Проверяет правильность получения объекта setting
        """
        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])

        setting = OrumSetting(type=self.types[2], orum=orum, power=3, hours=2, ratio=0.5)
        setting.installation_orum = self.periods[5]
        setting.removed_orum = self.periods[7]
        setting.save()
        setting = OrumSetting(type=self.types[2], orum=orum, power=3, hours=2, ratio=0.5)
        setting.installation_orum = self.periods[2]
        setting.removed_orum = self.periods[5]
        setting.save()

        self.assertEqual(orum.get_setting_in(self.periods[3]), setting)
        self.assertIsNone(orum.get_setting_in(self.periods[1]))
        self.assertIsNone(orum.get_setting_in(self.periods[7]))
        self.assertIsNone(orum.get_setting_in(self.periods[8]))

    def test_get_correction_in(self):
        """
        Проверяет правильность получения суммы корректировки kwh
        """
        orum = Orum.objects.create(point=self.point, installation_in_period=self.periods[1])
        OrumCorrection.objects.create(orum=orum, period=self.periods[3], kwh=3.001)
        OrumCorrection.objects.create(orum=orum, period=self.periods[3], kwh=2.001)
        OrumCorrection.objects.create(orum=orum, period=self.periods[5], kwh=4.0)

        self.assertEqual(orum.get_correction_in(self.periods[3]), 5.002)
        self.assertEqual(orum.get_correction_in(self.periods[2]), 0)
        self.assertEqual(orum.get_correction_in(self.periods[5]), 4)
