# coding: utf8
__author__ = 'Demyanov Kirill'
import fdb
from energy.models import Wire


con = fdb.connect(dsn=u'/home/kirill/Документы/Калугаэнерго/T2TEST.fdb', user='sysdba', password='masterkey')

cur = con.cursor()

select = """
select
    *
from
    TS_WIRE
"""

cur.execute(select)
for row in cur:
    print row[0]
    wire = Wire()
    wire.old_id = row[0]
    if row[1]:
        wire.title = row[1].decode('cp1251').encode('utf8')
    wire.ro = row[2]
    if row[3]:
        wire.comment = row[3].decode('cp1251').encode('utf8')
    wire.save()
