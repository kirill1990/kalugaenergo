# coding: utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.db.models import Q
from energy.models import Consumer

__author__ = 'Demyanov Kirill'


class ConsumerOrumList(DetailView):
    model = Consumer
    template_name = 'energy/consumer_orum.html'

    def get_context_data(self, **kwargs):
        context = super(ConsumerOrumList, self).get_context_data(**kwargs)

        context['period'] = self.object.production_area.power_grid_region.current_period

        points = self.object.point_set.filter(
            Q(meterorum__installation_in_period__lte=context['period'],
              meterorum__removed_in_period__gt=context['period'],)
            | Q(meterorum__installation_in_period__lte=context['period'],
                meterorum__removed_in_period__isnull=True)
        )

        context['orum_count'] = points.__len__()

        paginator = Paginator(points, 25)
        page = self.request.GET.get('page')
        try:
            points = paginator.page(page)
        except PageNotAnInteger:
            points = paginator.page(1)
        except EmptyPage:
            points = paginator.page(paginator.num_pages)
        context['points'] = points

        # context['points'] = context['object'].point_set.all()

        return context