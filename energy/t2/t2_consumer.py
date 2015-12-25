# coding: utf8
__author__ = 'Demyanov Kirill'
import fdb
from energy.models import Consumer, ConsumerType, ProductionArea


con = fdb.connect(dsn=u'/home/kirill/Документы/Калугаэнерго/T2TEST.fdb', user='sysdba', password='masterkey')

cur = con.cursor()

select = """
select
    ts_consumer.ls,
    ts_consumer.name
from
    ts_consumer
where
    ts_consumer.id_area in (36,37,38,39,40,41,42,43,68)
"""

cur.execute(select)
for row in cur:
    print row[0]
    consumer = Consumer()
    if row[1]:
        consumer.name = row[1].decode('cp1251').encode('utf8')
    if row[0]:
        consumer.ls = row[0].decode('cp1251').encode('utf8')
    consumer.type = ConsumerType.objects.get(pk=1)
    consumer.production_area = ProductionArea.objects.get(pk=1)
    consumer.save()
