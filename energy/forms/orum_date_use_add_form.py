# coding:utf8
from django import forms
from energy.models import Orum
from energy.models import Period

__author__ = 'Demyanov Kirill'

class OrumDateUseAddForm(forms.Form):
    orum = forms.ModelChoiceField(
        queryset=Orum.objects.all(),
    )
    period = forms.ModelChoiceField(
        queryset=Period.objects.all(),
    )
    date_use = forms.IntegerField(
        min_value=0,
        max_value=1000
    )
