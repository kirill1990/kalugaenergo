# coding: utf8
__author__ = 'Demyanov Kirill'
import fdb
from energy.models import Orum, OrumSetting, OrumType, Period, OrumCorrection, OrumDateUse
from decimal import Decimal


con = fdb.connect(dsn=u'/home/kirill/Документы/Калугаэнерго/T2TEST.fdb', user='sysdba', password='masterkey')

cur = con.cursor()
orumcalc = con.cursor()

orum_min = con.cursor()
orum_max = con.cursor()

select = """
select
    td_setuporum.id as id,              --  0
    td_setuporum.working as working,    --  1
    td_setuporum.deleted as deleted,    --  2
    td_setuporum.id_orumtype as type,   --  3
    ts_orumtype.formula as formula,     --  4
    td_setuporum."POWER" as power,      --  5
    td_setuporum.coef_use as ratio,     --  6
    td_setuporum.hour_use as hours      --  7
from
    td_setuporum
    left join ts_orumtype on ts_orumtype.id = td_setuporum.id_orumtype
"""

cur.execute(select)

# Or, equivalently:
# con = fdb.connect(
#     host='bison', database='/temp/test.db',
#     user='sysdba', password='pass'
#   )
# print cur.fetchall()

for row in cur:
    so_id = row[0]
    working = row[1]
    deleted = row[2]
    so_type = int(row[3])
    formula = int(row[4])
    power = row[5]
    ratio = row[6]
    hours = row[7]

    select2 = """
    select
        td_orumcalc.time_use as date_use,
        td_orumcalc.kwh as correction,
        td_orumcalc.id_period as period
    from
        td_orumcalc
    where
        td_orumcalc.id_setuporum = %s
    """

    sel_min = """
    select
        min(TD_ORUMCALC.ID_PERIOD)
    from
        TD_ORUMCALC
    where
        TD_ORUMCALC.id_setuporum = %s
    """

    sel_max = """
    select
        max(TD_ORUMCALC.ID_PERIOD)
    from
        TD_ORUMCALC
    where
        TD_ORUMCALC.id_setuporum = %s
    """

    orumcalc.execute(select2 % so_id)
    orum_min.execute(sel_min % so_id)
    orum_max.execute(sel_max % so_id)

    try:
        min_p = int(orum_min.next()[0])
        max_p = int(orum_max.next()[0])

        orum = Orum.objects.create(type=OrumType.objects.get(pk=so_type))

        setting = OrumSetting(orum=orum, power=power, hours=hours, ratio=ratio)
        setting.installation_orum = Period.objects.get(pk=(min_p+9))
        if max_p < 58:
            setting.removed_orum = Period.objects.get(pk=(max_p+10))
        setting.save()

        for row_calc in orumcalc:
            date_use = row_calc[0]
            correction = row_calc[1]
            period = int(row_calc[2])

            if correction:
                OrumCorrection.objects.create(orum=orum, period=Period.objects.get(pk=(period+9)), kwh=Decimal(correction))

            if date_use and formula in (2, 3):
                OrumDateUse.objects.create(orum=orum, period=Period.objects.get(pk=(period+9)), date_use=date_use)
    except:
        print so_id
