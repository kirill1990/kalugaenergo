from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from models import Message
from forms import MessageForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class IndexView(generic.ListView):
    template_name = 'journal/messages_list.html'
    context_object_name = 'messages_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Message.objects.order_by('number')[:5]

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MessageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MessageForm()

    return render(request, 'name.html', {'form': form})
