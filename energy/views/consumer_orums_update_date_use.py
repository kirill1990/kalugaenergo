# coding: utf-8
from django.http import JsonResponse
from django.views.generic import View
from energy.forms import OrumDateUseAddForm
from energy.models import OrumDateUse, Orum, Period

__author__ = 'Demyanov Kirill'

class OrumUpdateDateUse(View):
    def post(self, request, *args, **kwargs):
        data = {'kwh': 0}
        form = OrumDateUseAddForm(request.POST)

        if form.is_valid():
            orum = form.cleaned_data['orum']
            period = form.cleaned_data['period']
            date_use = request.POST['date_use']

            orum_date_use = OrumDateUse.objects.filter(orum=orum, period=period).first()
            if orum_date_use:
                orum_date_use.date_use = date_use
                orum_date_use.save()
            else:
                OrumDateUse.objects.create(orum=orum, period=period, date_use=date_use)
            data['kwh'] = orum.get_kwh_in(period)

        else:
            data = {'error': 2}

        return JsonResponse(data)
