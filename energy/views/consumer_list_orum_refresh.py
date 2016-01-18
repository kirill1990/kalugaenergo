# coding: utf-8
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import View
from energy.forms import PointPKForm
from energy.models import Period, Point

__author__ = 'Demyanov Kirill'

class ConsumerOrumRefresh(View):
    def post(self, request, *args, **kwargs):
        form = PointPKForm(request.POST)
        data = {}
        if form.is_valid():
            point = Point.objects.get(pk=request.POST['point'])
            period = Period.objects.get(pk=request.POST['period'])

            meter_orum = point.get_work(period)
            if meter_orum:
                orum = meter_orum.orum
                setting = orum.get_setting_in(period)
                # time.sleep(5)
                # data['title'] = point.name
                data['orum'] = orum.pk
                data['power'] = '%.3g' % setting.power
                data['ratio'] = '%.3g' % setting.ratio
                data['hours'] = setting.hours if orum.type.formula == 3 else '-'
                data['type_title'] = orum.type.title
                data['type_formula'] = orum.type.formula
                data['correction'] = orum.get_correction_in(period)
                data['date_use'] = orum.get_date_use(period) if orum.type.formula in (2, 3) else '-'
                data['kwh'] = orum.get_kwh_in(period)
                data['status'] = 0
            else:
                data['status'] = 1
        else:
            data['status'] = 2
        return JsonResponse(data)
