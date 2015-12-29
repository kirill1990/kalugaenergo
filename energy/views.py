# coding: utf-8
from django import views
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from energy.forms import ConsumerForm, PointForm
from energy.models import OrumDateUse, Orum, Period
from models import Consumer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ConsumerList(generic.ListView):
    template_name = 'energy/consumer_list.html'
    context_object_name = 'consumers_list'

    def get_queryset(self):
        consumers = Consumer.objects.all().order_by('ls')
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

class ConsumerDetail(DetailView):
    model = Consumer
    template_name = 'energy/consumer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ConsumerDetail, self).get_context_data(**kwargs)

        # Consumer.objects.get(**kwargs) point_set.all
        # context['pk'] = context['object'].pk
        context['period'] = context['object'].production_area.power_grid_region.current_period

        points = []
        for point in context['object'].point_set.all():
            obj = point.orum_in_current_period()
            if obj:
                points += [obj]

        context['points'] = points
        # context['pgr'] = Consumer.production_area.power_grid_region.title
        return context

def orum_date_use_update(request):
    if request.method == 'POST':
        form = PointForm(request.POST)

        if form.is_valid():
            orum = Orum.objects.get(pk=request.POST['orum'])
            period = Period.objects.get(pk=request.POST['period'])
            date_use = request.POST['date_use']

            orum_date_use = OrumDateUse.objects.filter(orum=orum, period=period).first()
            if orum_date_use:
                orum_date_use.date_use = date_use
                orum_date_use.save()
            else:
                OrumDateUse.objects.create(orum=orum, period=period, date_use=date_use)

            return HttpResponse(orum.get_kwh_in(period))

    return HttpResponse('fail')


class ConsumerCreate(CreateView):
    template_name = 'energy/consumer_add.html'
    form_class = ConsumerForm
    # success_url = 'energy/'

    def get_success_url(self):
        return reverse('energy:consumer_list')

    def form_valid(self, form):
        # Мы используем ModelForm, а его метод save() возвращает инстанс
        # модели, связанный с формой. Аргумент commit=False говорит о том, что
        # записывать модель в базу рановато.
        instance = form.save(commit=False)
        #
        # Теперь, когда у нас есть несохранённая модель, можно ей чего-нибудь
        # накрутить. Например, заполнить внешний ключ на auth.User. У нас же
        # блог, а не анонимный имижборд, правда?
        # instance.user = request.user
        #
        # А теперь можно сохранить в базу
        instance.save()

        # Consumer.objects.create(**form.cleaned_data)

        return redirect(self.get_success_url())
