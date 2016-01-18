# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from energy.forms import OrumSettingForm
from energy.models import Orum, Period

__author__ = 'Demyanov Kirill'

class OrumDetail(FormMixin, DetailView):
    model = Orum
    template_name = 'energy/consumer_orum_setting_add.html'
    form_class = OrumSettingForm

    def get_success_url(self):
        period = self.request.GET.get('period')
        pk = self.kwargs['pk']
        return "%s?period=%s" % (reverse('energy:orum_settings', kwargs={'pk': pk}), period)

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        form = OrumSettingForm(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            self.object = self.get_object()
            return self.form_valid(form)
        else:
            self.object = self.get_object()
            return self.form_invalid(form)

        # return (OrumDetail, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context = self.get_context_data()
        if context['setting']:
            form = OrumSettingForm(
                initial={
                    'ratio': context['setting'].ratio,
                    'power': context['setting'].power,
                    'hours': context['setting'].hours,
                }
            )
        # context['form']
            return self.form_invalid(form)
        # return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super(OrumDetail, self).get_context_data(**kwargs)
        period = get_object_or_404(Period, pk=self.request.GET.get('period'))

        context['setting'] = self.object.get_setting_in(period=period)
        # if context['setting']:
        #     context['form'] = OrumSettingForm(
        #         initial={
        #             'ratio': context['setting'].ratio,
        #             'power': context['setting'].power,
        #             'hours': context['setting'].hours,
        #         }
        #     )

        context['period'] = period
        context['settings'] = self.object.orumsetting_set.order_by('-installation_orum')

        return context

    # def get_context_data(self, **kwargs):
    #     context = super(OrumDetail, self).get_context_data(**kwargs)
    #     period = get_object_or_404(Period, pk=self.request.GET.get('period'))
    #
    #     context['setting'] = context['object'].get_setting_in(period=period)
    #     if context['setting']:
    #         context['form'] = OrumSettingForm(
    #             initial={
    #                 'ratio': context['setting'].ratio,
    #                 'power': context['setting'].power,
    #                 'hours': context['setting'].hours,
    #             }
    #         )
    #
    #     context['period'] = period
    #     context['settings'] = context['object'].orumsetting_set.order_by('-installation_orum')
    #
    #     return context