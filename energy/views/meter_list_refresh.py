# coding: utf-8
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import View
from energy.forms import PointPKForm
from energy.models import Period, Point

__author__ = 'Demyanov Kirill'

class MeterRefresh(View):
    def post(self, request, *args, **kwargs):
        form = PointPKForm(request.POST)
        data = {}
        if form.is_valid():
            point = form.cleaned_data['point']
            period = form.cleaned_data['period']

            meter = point.get_work_meter(period)
            if meter:
                data['number'] = meter.__str__()
                data['last_reading'] = meter.last_reading_for(period=period)
                data['reading'] = meter.reading_in(period=period)
                # setting = orum.get_setting_in(period)
                # time.sleep(5)
                # data['title'] = point.name
                # data['orum'] = orum.pk
                # data['power'] = '%.6g' % setting.power
                # data['ratio'] = '%.6g' % setting.ratio
                # data['hours'] = setting.hours if setting.type.formula == 3 else '-'
                # data['type_title'] = setting.type.title
                # data['type_formula'] = setting.type.formula
                # data['correction'] = orum.get_correction_in(period)
                # data['date_use'] = orum.get_date_use(period) if setting.type.formula in (2, 3) else '-'
                # data['kwh'] = orum.get_kwh_in(period)
                data['status'] = 0
            else:
                data['status'] = 1
        else:
            data['status'] = 2
        return JsonResponse(data)
