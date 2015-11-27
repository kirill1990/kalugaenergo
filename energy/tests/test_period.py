# coding: utf8
from django.test import TestCase
from energy.models import Period

__author__ = 'Demyanov Kirill'

class PeriodTest(TestCase):

    fixtures = ['energy_fixtures.json']

    def setUp(self):
        self.periods = {x: Period.objects.get(pk=x) for x in range(1, 11)}

    def test_count(self):
        """ Наличие периодов в бд """
        self.assertNotEqual(Period.objects.all().count(), 0)

    def test_between_left(self):
        """ Проверяемый период находится левее проверяемой временной линии """
        self.assertFalse(self.periods[3].between(self.periods[4], self.periods[7]))
        self.assertFalse(self.periods[2].between(self.periods[3], None))

    def test_between_right(self):
        """ Проверяемый период находится правее проверяемой временной линии """
        self.assertFalse(self.periods[4].between(self.periods[2], self.periods[3]))
        self.assertFalse(self.periods[3].between(self.periods[2], self.periods[3]))

    def test_between_into(self):
        """ Проверяемый период находится внутри проверяемой временной линии """
        self.assertTrue(self.periods[3].between(self.periods[1], self.periods[5]))
        self.assertTrue(self.periods[3].between(self.periods[3], self.periods[4]))
        self.assertTrue(self.periods[4].between(self.periods[2], None))
