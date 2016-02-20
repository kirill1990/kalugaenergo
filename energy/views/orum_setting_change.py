# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.views.generic.edit import FormMixin

from energy.forms import OrumSettingForm
from energy.models import Orum, Period, OrumType

__author__ = 'Demyanov Kirill'

class OrumDetail(View):
    template_name = 'energy/consumer_orum_setting_change.html'
    form_class = OrumSettingForm

    def post(self, request, *args, **kwargs):
        form = OrumSettingForm(request.POST, prefix='setting')
        context = self.get_context_data(**kwargs)
        if form.is_valid():
            orum_type = form.cleaned_data['orum_type']
            period = context['period']
            setting = context['orum'].get_setting_in(period=period)

            if setting.installation_orum != period:
                period_old = setting.removed_orum
                setting.removed_orum = period
                setting.save()

                setting.id = None
                setting.installation_orum = period
                setting.removed_orum = period_old

            setting.type = orum_type
            setting.ratio = form.cleaned_data['ratio']
            setting.power = form.cleaned_data['power']
            setting.hours = form.cleaned_data['hours']
            setting.save()

        context['form'] = form

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        setting = context['orum'].get_setting_in(context['period'])
        if setting:
            context['form'] = OrumSettingForm(
                initial={
                    'orum_type': setting.type.pk,
                    'ratio': setting.get_ratio(),
                    'power': setting.get_power(),
                    'hours': setting.hours,
                },
                prefix='setting',
            )
        return render(request, self.template_name, context)

    @staticmethod
    def get_context_data(**kwargs):
        orum = get_object_or_404(Orum, **kwargs)
        period = orum.point.consumer.current_period()

        return {
            'period': period,
            'settings': orum.orumsetting_set.order_by('-installation_orum'),
            'orum': orum,
        }
