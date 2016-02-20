# coding: utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django.db.models import Q
from energy.models import Consumer

__author__ = 'Demyanov Kirill'


class MeterList(DetailView):
    model = Consumer
    template_name = 'energy/consumer_meters.html'

    def get_context_data(self, **kwargs):
        context = super(MeterList, self).get_context_data(**kwargs)

        context['period'] = self.object.production_area.power_grid_region.current_period

        points = self.object.point_set.filter(
            Q(pointmeter__installation_in_period__lte=context['period'],
              pointmeter__removed_in_period__gt=context['period'],)
            | Q(pointmeter__installation_in_period__lte=context['period'],
                pointmeter__removed_in_period__isnull=True)
        )

        # points = self.object.point_set.all()

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
