# coding: utf8
__author__ = 'Demyanov Kirill'
import fdb
from energy.models import Transformer


con = fdb.connect(dsn=u'/home/kirill/Документы/Калугаэнерго/T2TEST.fdb', user='sysdba', password='masterkey')

cur = con.cursor()

select = """
select
    *
from
    TS_TRANSFORMATOR
"""

cur.execute(select)
for row in cur:
    print row[0]
    trans = Transformer()
    trans.old_id = row[0]
    if row[1]:
        trans.title = row[1].decode('cp1251').encode('utf8')
    trans.pxx = row[2]
    trans.pkz = row[3]
    trans.s = row[4]
    if row[5]:
        trans.comment = row[5].decode('cp1251').encode('utf8')
    trans.save()
