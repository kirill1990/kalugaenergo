# coding: utf-8
from django.views import generic
from energy.models import Legal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Legals(generic.ListView):
    template_name = 'energy/legals.html'
    context_object_name = 'legals'

    def get_queryset(self):
        legals = Legal.objects.order_by('ls')

        search = self.request.GET.get('search')
        if search:
            legals = legals.filter(ls__icontains=search)

        paginator = Paginator(legals, 100)
        page = self.request.GET.get('page')
        try:
            legals = paginator.page(page)
        except PageNotAnInteger:
            legals = paginator.page(1)
        except EmptyPage:
            legals = paginator.page(paginator.num_pages)
        return legals

    def get_context_data(self, **kwargs):
        context = super(Legals, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        context['search'] = search if search else ''
        return context
