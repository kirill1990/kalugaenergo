# coding: utf8
from django.test import TestCase
from energy.models.period import Period
from energy.models.production_area import ProductionArea
from energy.models.meter import Meter
from energy.models.meter_passport import MeterPassport
from energy.models.meter_reading import MeterReading
from energy.models.meter_reading_event import MeterReadingEvent
from energy.models.meter_correction import MeterCorrection
from energy.models.meter_setting import MeterSetting
from energy.models.transformer import Transformer
from energy.models.wire import Wire

__author__ = 'Demyanov Kirill'

class TestMeter(TestCase):
    fixtures = ['energy_fixtures']

    def setUp(self):
        self.periods = {x: Period.objects.get(pk=x) for x in range(1, 16)}
        self.events = {x: MeterReadingEvent.objects.get(pk=x) for x in range(1, 6)}
        self.power_grid_region = ProductionArea.objects.create(
            title='test',
            current_period=self.periods[6],
        )
        self.passport = MeterPassport.objects.get(pk=1)

        self.meter = Meter.objects.create(
            serial_number='1',
            power_grid_region=self.power_grid_region,
            passport=self.passport
        )

        transformer = Transformer.objects.create(old_id=1, title='test', pxx=1.31, pkz=7.6, s=400)
        wire = Wire.objects.create(old_id=1, title='test', ro=1.25)

        self.setting_meters = {
            1: MeterSetting.objects.create(
                meter=self.meter,
                installation_meter_setting=self.periods[3],
                removed_meter_setting=self.periods[5],
                c_loss=1.1,
                c_trans=1.2,
                type_of_energy=0,
                direction_energy=1,
                meter_place=0,
            ),
            2: MeterSetting.objects.create(
                meter=self.meter,
                installation_meter_setting=self.periods[5],
                removed_meter_setting=self.periods[6],
                c_loss=1.1,
                c_trans=1.2,
                type_of_energy=0,
                direction_energy=1,
                meter_place=0,
                tangfi=0.9,
            ),
            3: MeterSetting.objects.create(
                meter=self.meter,
                installation_meter_setting=self.periods[6],
                removed_meter_setting=self.periods[10],
                c_loss=1.1,
                c_trans=1.2,
                type_of_energy=0,
                direction_energy=1,
                meter_place=0,
                cosfi=0.7,
                tangfi=0.9,
                transformer=transformer,
                work_hours=1,
            ),
            4: MeterSetting.objects.create(
                meter=self.meter,
                installation_meter_setting=self.periods[10],
                removed_meter_setting=self.periods[12],
                c_loss=1.1,
                c_trans=1.2,
                type_of_energy=0,
                direction_energy=1,
                meter_place=0,
                wire=wire,
                wire_length=200,
                wire_voltage=2,
            ),
        }

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

    def test_reading(self):
        """ Проверка получения показаний за выбранный период """

        # начального показания
        self.assertEqual(self.meter.reading_for(self.periods[2]), 100)

        # показания за период только с одним показанием
        self.assertEqual(self.meter.reading_for(self.periods[9]), 125)

        # показания за период с несколькими показаниями
        self.assertEqual(self.meter.reading_for(self.periods[10]), 135)

        # показаний по приоритету
        self.assertEqual(self.meter.reading_for(self.periods[3]), 103)

        # на жесткий выбор используемого показания
        self.assertEqual(self.meter.reading_for(self.periods[4]), 113)

        # показания в период без данных
        self.assertEqual(self.meter.reading_for(self.periods[5]), 113)
        self.assertEqual(self.meter.reading_for(self.periods[8]), 120)

        # показания которое перешло через ноль
        self.assertEqual(self.meter.reading_for(self.periods[11]), 44)

    def test_last_reading(self):
        """ Проверка получения показаний за прошлый период """

        # начального показания
        self.assertEqual(self.meter.last_reading_for(self.periods[3]), 100)

        # показания за период только с одним показанием
        self.assertEqual(self.meter.last_reading_for(self.periods[10]), 125)

        # показания за период с несколькими показаниями
        self.assertEqual(self.meter.last_reading_for(self.periods[11]), 135)

        # показаний по приоритету
        self.assertEqual(self.meter.last_reading_for(self.periods[4]), 103)

        # жесткий выбор используемого показания
        self.assertEqual(self.meter.last_reading_for(self.periods[5]), 113)

        # показания в период без данных
        self.assertEqual(self.meter.last_reading_for(self.periods[6]), 113)

    def test_correction_in(self):
        """ Проверка получение суммы корректировки kwh за период """

        MeterCorrection.objects.bulk_create([
            MeterCorrection(meter=self.meter, period=self.periods[3], kwh=3.001),
            MeterCorrection(meter=self.meter, period=self.periods[3], kwh=3.001),
            MeterCorrection(meter=self.meter, period=self.periods[4], kwh=2.6)
        ])

        self.assertEqual(self.meter.correction_in(self.periods[3]), 6.002)
        self.assertEqual(self.meter.correction_in(self.periods[4]), 2.6)
        self.assertEqual(self.meter.correction_in(self.periods[5]), 0)

    def test_setting_in(self):
        """ Проверка выбора параметров установки счетчика за указанный период """

        # нахождения настроек в нужном периоде
        self.assertEqual(self.meter.setting_in(self.periods[2]), None)
        for index in range(3, 5):
            self.assertEqual(self.meter.setting_in(self.periods[index]), self.setting_meters[1])
        for index in range(5, 6):
            self.assertEqual(self.meter.setting_in(self.periods[index]), self.setting_meters[2])
        for index in range(6, 10):
            self.assertEqual(self.meter.setting_in(self.periods[index]), self.setting_meters[3])
        for index in range(10, 12):
            self.assertEqual(self.meter.setting_in(self.periods[index]), self.setting_meters[4])
        self.assertEqual(self.meter.setting_in(self.periods[15]), None)

        # нахождения настроек не находится не в своем периоде
        for index in range(1, 16):
            if index not in (3, 4):
                self.assertNotEqual(self.meter.setting_in(self.periods[index]), self.setting_meters[1])
            if index != 5:
                self.assertNotEqual(self.meter.setting_in(self.periods[index]), self.setting_meters[2])
            if index not in (6, 7, 8, 9):
                self.assertNotEqual(self.meter.setting_in(self.periods[index]), self.setting_meters[3])
            if index not in (10, 11):
                self.assertNotEqual(self.meter.setting_in(self.periods[index]), self.setting_meters[4])

    def test_kwh_meter(self):
        """ Проверка получения kwh за период по счетчику """

        # показания в обычном режиме
        self.assertEqual(self.meter.last_reading_for(self.periods[4]), 103)
        self.assertEqual(self.meter.reading_for(self.periods[4]), 113)
        self.assertEqual(self.meter.kwh_meter(self.periods[4]), 10)

        # показания, которое перешло через ноль
        self.assertEqual(self.meter.last_reading_for(self.periods[11]), 135)
        self.assertEqual(self.meter.reading_for(self.periods[11]), 44)
        self.assertEqual(self.meter.kwh_meter(self.periods[11]), 9999909)

        # за период, в котором не было показаний
        self.assertEqual(self.meter.last_reading_for(self.periods[5]), 113)
        self.assertEqual(self.meter.reading_for(self.periods[5]), 113)
        self.assertEqual(self.meter.kwh_meter(self.periods[5]), 0)

        self.assertEqual(self.meter.kwh_meter(self.periods[6]), 7)
        self.assertEqual(self.meter.kwh_meter(self.periods[10]), 10)

    def test_kwh_consumption(self):
        """ Проверка kwh с учетом коэффициентов потребления и потерь за период по счетчику """

        # показания в обычном режиме
        self.assertEqual(self.meter.last_reading_for(self.periods[4]), 103)
        self.assertEqual(self.meter.reading_for(self.periods[4]), 113)
        self.assertEqual(self.meter.kwh_consumption(self.periods[4]), 13.2)

        # показания, которое перешло через ноль
        self.assertEqual(self.meter.last_reading_for(self.periods[11]), 135)
        self.assertEqual(self.meter.reading_for(self.periods[11]), 44)
        self.assertEqual(self.meter.kwh_consumption(self.periods[11]), 13199879.88)

        # за период, в котором не было показаний
        self.assertEqual(self.meter.last_reading_for(self.periods[5]), 113)
        self.assertEqual(self.meter.reading_for(self.periods[5]), 113)
        self.assertEqual(self.meter.kwh_consumption(self.periods[5]), 0)

        self.assertEqual(self.meter.kwh_consumption(self.periods[6]), 9.24)
        self.assertEqual(self.meter.kwh_consumption(self.periods[10]), 13.2)

    def test_cosfi(self):
        """ Проверка косинуса фи """

        # в настройка не указан
        self.assertEqual(self.meter.cosfi(self.setting_meters[1]), 0.8)
        # указан тангенс фи
        self.assertEqual(self.meter.cosfi(self.setting_meters[2]), 0.743294146)
        # указан косинус фи
        self.assertEqual(self.meter.cosfi(self.setting_meters[3]), 0.7)

    def test_loss_in_wire(self):
        # TODO добавить тесты потерь в линии
        self.assertEqual(self.meter.loss_in_wire_period(self.periods[3]), 0)
        self.assertEqual(self.meter.loss_in_wire_period(self.periods[10]), 0.023)

    def test_loss_in_transformer(self):
        # TODO добавить тесты потерь в трансформаторе
        self.assertEqual(self.meter.loss_in_transformer_period(self.periods[3]), 0)
        self.assertEqual(self.meter.loss_in_transformer_period(self.periods[6]), 943.208)

