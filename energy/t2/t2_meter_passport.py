# coding: utf8
__author__ = 'Demyanov Kirill'
import fdb
from energy.models import MeterPassport


con = fdb.connect(dsn=u'/home/kirill/Документы/Калугаэнерго/T2TEST.fdb', user='sysdba', password='masterkey')

cur = con.cursor()

select = """
select
   --FIRST 20
  *
from
  ts_metertype
"""
select += """
where
id = 12153
"""


cur.execute(select)
for row in cur:
    print row[0]
    meter = MeterPassport()
    meter.old_id = row[0]
    if row[1]:
        meter.title = row[1].decode('cp1251').encode('utf8')
    meter.digits = row[2]
    meter.decimals = row[3]
    meter.check_period = row[4]
    meter.replace_period = row[5]
    meter.phase = row[6]
    meter.tariff = row[7]
    meter.type_of_meter = row[8]
    meter.accuracy_class = row[9]
    if row[10]:
        meter.voltage = row[10].decode('cp1251').encode('utf8')
    if row[11]:
        meter.amperage = row[11].decode('cp1251').encode('utf8')
    meter.type_of_energy = row[12] - 1
    meter.direct = row[13]
    if row[14]:
        meter.comment = row[14].decode('cp1251').encode('utf8')

    meter.check = row[15]
    # meter.check = 1
    if row[19] == 1:
        meter.active = 0
    else:
        meter.active = 1

    meter.save()

