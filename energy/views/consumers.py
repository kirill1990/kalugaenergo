# coding: utf-8
from django.views import generic
from energy.models import Consumer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Consumers(generic.ListView):
    template_name = 'energy/consumers.html'
    context_object_name = 'consumers'

    def get_queryset(self):
        consumers = Consumer.objects.filter(type=0).order_by('ls')

        search = self.request.GET.get('search')
        if search:
            consumers = consumers.filter(ls__icontains=search)

        paginator = Paginator(consumers, 100)
        page = self.request.GET.get('page')
        try:
            consumers = paginator.page(page)
        except PageNotAnInteger:
            consumers = paginator.page(1)
        except EmptyPage:
            consumers = paginator.page(paginator.num_pages)
        return consumers

    def get_context_data(self, **kwargs):
        context = super(Consumers, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        context['search'] = search if search else ''
        return context
