# coding: utf8
from django.test import TestCase
from energy.models import Orum, OrumType, Period, OrumValue

__author__ = 'Demyanov Kirill'

# Create your tests here.
class OrumTest(TestCase):
    fixtures = ['energy_fixtures']

    def setUp(self):
        self.types = {OrumType.objects.get(pk=x).formula: OrumType.objects.get(pk=x) for x in range(6, 9)}
        self.periods = {x: Period.objects.get(pk=x) for x in range(1, 11)}

    def test_valid_orum_type(self):
        """ Для орумов предусмотрено 8 типов """
        self.assertEqual(OrumType.objects.all().count(), 8)

    def test_hours_default_equal_1(self):
        """ В орумах часы использования по умолчанию 1 """
        orum = Orum.objects.create(type=self.types[1], power=0.0001, installation_in_period=self.periods[1])
        self.assertEqual(orum.hours, 1)

    def test_ratio_default_equal_1(self):
        """ В орумах коэффициент по умолчанию 1 """
        orum = Orum.objects.create(type=self.types[1], power=0.0001, installation_in_period=self.periods[1])
        self.assertEqual(orum.ratio, 1)

    def test_none_period(self):
        """ Запрос по периоду, в котором не было/нет орума """
        orum = Orum(type=self.types[1], power=0.0001)
        orum.installation_in_period = self.periods[3]
        orum.removed_in_period = self.periods[5]
        orum.save()

        self.assertEqual(orum.value(self.periods[2]), None)
        self.assertEqual(orum.value(self.periods[5]), None)
        self.assertEqual(orum.value(self.periods[6]), None)

    def test_value_orum_formula_1(self):
        """
        Проверяет правильность вычисления потребления
        орумов по формуле 1:
            kwh = [Мощность]
                        * [Коэффициент]
                        + [Корректировка в kwh]
        """

        """ Задана только [Мощность] """
        orum = Orum.objects.create(type=self.types[1], power=0.0001, installation_in_period=self.periods[1])
        self.assertEqual(orum.type.formula, 1)
        self.assertEqual(orum.value(self.periods[1]), 0.0001)
        self.assertEqual(orum.value(self.periods[2]), 0.0001)

        """ + [Коэффициент] """
        orum.ratio = 0.1
        self.assertEqual(orum.value(self.periods[3]), 0.00001)

        """ + [Корректировка в kwh] """
        OrumValue.objects.create(orum=orum, period=self.periods[4], kwh=1.34)
        self.assertEqual(orum.value(self.periods[4]), 1.34001)

    def test_value_orum_formula_2(self):
        """
        Проверяет правильность вычисления потребления
        орумов по формуле 2:
            kwh = [Мощность]
                        * [Количество дней в использование]
                        * [Коэффициент]
                        + [Корректировка в kwh]
        """
        orum = Orum.objects.create(type=self.types[2], power=0.0001, installation_in_period=self.periods[1])
        self.assertEqual(orum.type.formula, 2)

        """ Задана только [Мощность] """
        self.assertEqual(orum.value(self.periods[1]), 0.0001)

        """ Задана только [Мощность] """
        orum = Orum.objects.create(type=self.types[2], power=0.0001, installation_in_period=self.periods[1])
        OrumValue.objects.create(orum=orum, period=self.periods[1], date_use=3)
        self.assertEqual(orum.value(self.periods[1]), 0.0003)

        OrumValue.objects.create(orum=orum, period=self.periods[2], date_use=3, kwh=3.23)
        self.assertEqual(orum.value(self.periods[2]), 3.2303)

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
        orum = Orum.objects.create(type=self.types[3], power=0.0001, installation_in_period=self.periods[1])

        """ Задана только [Мощность] """
        self.assertEqual(orum.type.formula, 3)
        self.assertEqual(orum.value(self.periods[1]), 0.0001)

        """ Задана только [Мощность] и [Количество дней в использование] """
        orum = Orum.objects.create(type=self.types[3], power=0.0001, installation_in_period=self.periods[1])
        OrumValue.objects.create(orum=orum, period=self.periods[1], date_use=3)
        self.assertEqual(orum.value(self.periods[1]), 0.0003)

        OrumValue.objects.create(orum=orum, period=self.periods[2], date_use=3, kwh=3.23)
        self.assertEqual(orum.value(self.periods[2]), 3.2303)

        """ c [Время использования в день] """
        orum = Orum.objects.create(type=self.types[3], power=0.0001, hours=3, installation_in_period=self.periods[1])
        OrumValue.objects.create(orum=orum, period=self.periods[1], date_use=3)
        self.assertEqual(orum.value(self.periods[1]), 0.0009)

        OrumValue.objects.create(orum=orum, period=self.periods[2], date_use=3, kwh=3.23)
        self.assertEqual(orum.value(self.periods[2]), 3.2309)

