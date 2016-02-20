# coding: utf8
__author__ = 'Demyanov Kirill'
import fdb
from energy.models import Consumer, ConsumerType, ProductionArea, Point
from energy.models import Orum, OrumSetting, OrumType, Period, OrumCorrection, OrumDateUse, PointMeter
from decimal import Decimal

con = fdb.connect(dsn=u'/home/kirill/Документы/Калугаэнерго/T2TEST.fdb', user='sysdba', password='masterkey')

t2_consumers = con.cursor()
t2_points = con.cursor()

orumcalc = con.cursor()
orum_min = con.cursor()
orum_max = con.cursor()

select = """
select
    first 2000
    ts_consumer.ls,
    ts_consumer.name,
    ts_consumer.id
from
    ts_consumer
where
    ts_consumer.id_area in (36,37,38,39,40,41,42,43,68)
    and ts_consumer.is_byt = 0
"""
    # and ts_consumer.id = 402
    # and ts_consumer.id = 9674

t2_consumers.execute(select)
for t2_consumer in t2_consumers:
    consumer = Consumer()
    consumer.old_id = t2_consumer[2]
    if t2_consumer[1]:
        consumer.name = t2_consumer[1].decode('cp1251').encode('utf8')
    if t2_consumer[0]:
        print 'ls: %s' % t2_consumer[0]
        consumer.ls = t2_consumer[0].decode('cp1251').encode('utf8')
    consumer.type = ConsumerType.objects.get(pk=1)
    consumer.production_area = ProductionArea.objects.get(pk=1)
    consumer.save()

    point_select = """
    select
        td_setuporum.id as id,              --  0
        td_setuporum.working as working,    --  1
        td_setuporum.deleted as deleted,    --  2
        td_setuporum.id_orumtype as type,   --  3
        ts_orumtype.formula as formula,     --  4
        td_setuporum."POWER" as power,      --  5
        td_setuporum.coef_use as ratio,     --  6
        td_setuporum.hour_use as hours,     --  7
        ts_point.id,
        ts_point.name,
        td_setupconsumer.id_period_ins,
        td_setupconsumer.id_period_rem
    from
        td_setupconsumer
        left join ts_point on ts_point.id = td_setupconsumer.id_point
        left join td_setuporum on td_setuporum.id_point = ts_point.id
        left join ts_orumtype on ts_orumtype.id = td_setuporum.id_orumtype
    where
        td_setupconsumer.id_consumer = %s
        and td_setuporum.id is not null
    """
        # and ts_point.id = 1240

    t2_points.execute(point_select % consumer.old_id)

    for t2_point in t2_points:

        so_id = t2_point[0]
        working = t2_point[1]
        deleted = t2_point[2]
        so_type = int(t2_point[3])
        formula = int(t2_point[4])
        power = t2_point[5]
        ratio = t2_point[6]
        hours = t2_point[7]
        point_old_id = t2_point[8]
        point_title = t2_point[9]
        per_ins = t2_point[10]
        per_rem = t2_point[11]

        if per_rem is None:
            per_rem = 999

        point = Point.objects.filter(number_in_t2=point_old_id).first()
        # print point

        if point is None:
            # print u'point'
            point = Point()
            point.consumer = consumer
            point.number_in_t2 = point_old_id
            if point_title:
                point.title = point_title.decode('cp1251').encode('utf8')
            point.save()

        # print u'point:%s   old:%s' % (point.pk, point_old_id)

        select2 = """
        select
            td_orumcalc.time_use as date_use,
            td_orumcalc.kwh as correction,
            td_orumcalc.id_period as period
        from
            td_orumcalc
        where
            td_orumcalc.id_setuporum = %s
            and td_orumcalc.id_period >= %s
            and (td_orumcalc.id_period < %s or td_orumcalc.id_period is null)
        """

        sel_min = """
        select
            min(TD_ORUMCALC.ID_PERIOD)
        from
            TD_ORUMCALC
        where
            TD_ORUMCALC.id_setuporum = %s
            and td_orumcalc.id_period >= %s
            and (td_orumcalc.id_period < %s or td_orumcalc.id_period is null)
        """

        sel_max = """
        select
            max(TD_ORUMCALC.ID_PERIOD)
        from
            TD_ORUMCALC
        where
            TD_ORUMCALC.id_setuporum = %s
            and td_orumcalc.id_period >= %s
            and (td_orumcalc.id_period < %s or td_orumcalc.id_period is null)
        """

        orumcalc.execute(select2 % (so_id, per_ins, per_rem))
        orum_min.execute(sel_min % (so_id, per_ins, per_rem))
        orum_max.execute(sel_max % (so_id, per_ins, per_rem))

        # try:
        min_p_tmp = orum_min.next()[0]
        max_p_tmp = orum_max.next()[0]

        if min_p_tmp and max_p_tmp:

            point = Point.objects.filter(number_in_t2=point_old_id).first()
            # print point

            if point is None:
                # print u'point'
                point = Point()
                point.consumer = consumer
                point.number_in_t2 = point_old_id
                if point_title:
                    point.title = point_title.decode('cp1251').encode('utf8')
                point.save()

            # print u'point:%s;old:%s' % (point.pk, point_old_id)

            min_p = int(min_p_tmp)
            max_p = int(max_p_tmp)

            period_ins = Period.objects.get(pk=(min_p+9))
            period_rem = None
            if max_p < 58:
                period_rem = Period.objects.get(pk=(max_p+10))

            orum = Orum.objects.filter(point=point).first()

            if orum is None:
                orum = Orum.objects.create(
                    point=point,
                    installation_in_period=period_ins,
                )

            if max_p < 58:
                orum.removed_in_period = period_rem
            else:
                orum.removed_in_period = None
            orum.save()

            setting = OrumSetting(
                type=OrumType.objects.get(pk=so_type),
                orum=orum,
                power=power,
                hours=hours,
                ratio=ratio,
            )
            setting.installation_orum = period_ins
            setting.removed_orum = period_rem
            setting.save()

            # print 'point: %s' % t2_point[8]

            for row_calc in orumcalc:
                date_use = row_calc[0]
                correction = row_calc[1]
                period = int(row_calc[2])

                if correction:
                    OrumCorrection.objects.create(
                        orum=orum,
                        period=Period.objects.get(pk=(period+9)),
                        kwh=Decimal(correction),
                    )

                if date_use and formula in (2, 3):
                    try:
                        OrumDateUse.objects.create(
                            orum=orum,
                            period=Period.objects.get(pk=(period+9)),
                            date_use=date_use,
                        )
                    except Exception as e:
                        print '%s (%s)' % (e.message, type(e))
                        print '%s period %s' % (orum, period)
                        print 'duplicate date use: %s' % so_id
        #     print 'point: %s, so_id:%s' % (t2_point[8], so_id)

print 'done'