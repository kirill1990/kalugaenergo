# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View

from energy.forms import OrumSettingForm, PointForm
from energy.models import Legal, Orum, Point, OrumSetting

__author__ = 'Demyanov Kirill'

class OrumAdd(View):
    template_name = 'energy/consumer_orum_add.html'
    form_class = OrumSettingForm

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form_setting = OrumSettingForm(request.POST, prefix='setting')
        form_point = PointForm(request.POST, prefix='point')

        if form_setting.is_valid() and form_point.is_valid():
            point = Point.objects.create(
                consumer=context['consumer'],
                title=form_point.cleaned_data['title'],
            )

            orum = Orum.objects.create(
                point=point,
                installation_in_period=context['period'],
            )

            OrumSetting.objects.create(
                orum=orum,
                type=form_setting.cleaned_data['orum_type'],
                installation_orum=context['period'],
                ratio=form_setting.cleaned_data['ratio'],
                power=form_setting.cleaned_data['power'],
                hours=form_setting.cleaned_data['hours'],
            )

            return redirect(reverse('energy:consumer_orum_list', kwargs={'pk': context['consumer'].pk}))

        context['form_setting'] = form_setting
        context['form_point'] = form_point
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        setting = OrumSettingForm(
            initial={
                'orum_type': 7,
            },
            prefix='setting',
        )
        point = PointForm(
            prefix='point',
        )

        context['form_setting'] = setting
        context['form_point'] = point

        return render(request, self.template_name, context)

    @staticmethod
    def get_context_data(**kwargs):
        consumer = get_object_or_404(Consumer, **kwargs)
        period = consumer.current_period()

        return {
            'period': period,
            'consumer': consumer,
        }
