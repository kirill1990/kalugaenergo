# coding: utf-8
from django.views import generic
from energy.models import ConsumerType
from energy.models import Consumer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ConsumerList(generic.ListView):
    template_name = 'energy/consumer_list.html'
    context_object_name = 'consumers_list'

    def get_queryset(self):
        consumer_type = ConsumerType.objects.get_or_create(pk=1)
        consumers = Consumer.objects.filter(type=consumer_type[0]).order_by('ls')

        search = self.request.GET.get('search')
        if search:
            consumers = consumers.filter(ls__icontains=search)

        paginator = Paginator(consumers, 100)
        page = self.request.GET.get('page')
        try:
            consumers = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            consumers = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            consumers = paginator.page(paginator.num_pages)
        return consumers

    def get_context_data(self, **kwargs):
        context = super(ConsumerList, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        context['search'] = search if search else ''
        return context