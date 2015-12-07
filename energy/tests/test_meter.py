# coding: utf8
from django.test import TestCase
from energy.models import Period, Meter, \
    PowerGridRegion, \
    MeterReading,MeterReadingEvent, MeterPassport
from energy.models.meter_correction import MeterCorrection

__author__ = 'Demyanov Kirill'

class TestMeter(TestCase):
    fixtures = ['energy_fixtures']

    def setUp(self):
        self.periods = {x: Period.objects.get(pk=x) for x in range(1, 16)}
        self.events = {x: MeterReadingEvent.objects.get(pk=x) for x in range(1, 6)}
        self.res = PowerGridRegion.objects.create(title='test', current_period=self.periods[6])
        self.passport = MeterPassport.objects.get(pk=1)

        self.meter = Meter.objects.create(serial_number='1', res=self.res, passport=self.passport)

        MeterReading.objects.bulk_create([
            MeterReading(meter=self.meter, event=self.events[1], reading=100, period=self.periods[3]),
            MeterReading(meter=self.meter, event=self.events[4], reading=105, period=self.periods[3]),
            MeterReading(meter=self.meter, event=self.events[3], reading=103, period=self.periods[3]),
            MeterReading(meter=self.meter, event=self.events[4], reading=106, period=self.periods[3]),
            MeterReading(meter=self.meter, event=self.events[5], reading=101, period=self.periods[3]),
            MeterReading(meter=self.meter, event=self.events[4], reading=110, period=self.periods[4]),
            MeterReading(meter=self.meter, event=self.events[3], reading=116, period=self.periods[4]),
            MeterReading(meter=self.meter, event=self.events[4], reading=113, period=self.periods[4], is_true=True),
            MeterReading(meter=self.meter, event=self.events[4], reading=120, period=self.periods[6]),
            MeterReading(meter=self.meter, event=self.events[4], reading=125, period=self.periods[9]),
            MeterReading(meter=self.meter, event=self.events[4], reading=131, period=self.periods[10]),
            MeterReading(meter=self.meter, event=self.events[4], reading=135, period=self.periods[10]),
            MeterReading(meter=self.meter, event=self.events[4], reading=133, period=self.periods[10]),
            MeterReading(meter=self.meter, event=self.events[4], reading=44, period=self.periods[11]),
        ])

    def test_get_reading(self):
        """ Проверка получения показаний за выбранный период """

        # начального показания
        self.assertEqual(self.meter.get_reading_for(self.periods[2]), 100)

        # показания за период только с одним показанием
        self.assertEqual(self.meter.get_reading_for(self.periods[9]), 125)

        # показания за период с несколькими показаниями
        self.assertEqual(self.meter.get_reading_for(self.periods[10]), 135)

        # показаний по приоритету
        self.assertEqual(self.meter.get_reading_for(self.periods[3]), 103)

        # на жесткий выбор используемого показания
        self.assertEqual(self.meter.get_reading_for(self.periods[4]), 113)

        # показания в период без данных
        self.assertEqual(self.meter.get_reading_for(self.periods[5]), 113)
        self.assertEqual(self.meter.get_reading_for(self.periods[8]), 120)

        # показания которое перешло через ноль
        self.assertEqual(self.meter.get_reading_for(self.periods[11]), 44)

    def test_get_last_reading(self):
        """ Проверка получения показаний за прошлый период """

        # начального показания
        self.assertEqual(self.meter.get_last_reading_for(self.periods[3]), 100)

        # показания за период только с одним показанием
        self.assertEqual(self.meter.get_last_reading_for(self.periods[10]), 125)

        # показания за период с несколькими показаниями
        self.assertEqual(self.meter.get_last_reading_for(self.periods[11]), 135)

        # показаний по приоритету
        self.assertEqual(self.meter.get_last_reading_for(self.periods[4]), 103)

        # жесткий выбор используемого показания
        self.assertEqual(self.meter.get_last_reading_for(self.periods[5]), 113)

        # показания в период без данных
        self.assertEqual(self.meter.get_last_reading_for(self.periods[6]), 113)

    def test_get_correction_in(self):
        MeterCorrection.objects.bulk_create([
            MeterCorrection(meter=self.meter, period=self.periods[3], kwh=3.001),
            MeterCorrection(meter=self.meter, period=self.periods[3], kwh=3.001),
            MeterCorrection(meter=self.meter, period=self.periods[4], kwh=2.6)
        ])

        self.assertEqual(self.meter.get_correction_in(self.periods[3]), 6.002)
        self.assertEqual(self.meter.get_correction_in(self.periods[4]), 2.6)
        self.assertEqual(self.meter.get_correction_in(self.periods[5]), 0)
