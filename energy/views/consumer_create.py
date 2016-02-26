# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from energy.forms import LegalForm

__author__ = 'Demyanov Kirill'

class ConsumerCreate(CreateView):
    template_name = 'energy/consumer_add.html'
    form_class = LegalForm
    # success_url = 'energy/'

    # def get_success_url(self):
    #     return reverse('energy:consumer')

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

        return redirect(reverse('energy:consumer', kwargs={'pk': instance.pk}))
