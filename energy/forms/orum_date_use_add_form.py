# coding:utf8
from django import forms

__author__ = 'Demyanov Kirill'

class OrumDateUseAddForm(forms.Form):
    orum = forms.IntegerField()
    period = forms.IntegerField()
    date_use = forms.IntegerField(min_value=0, max_value=1000)