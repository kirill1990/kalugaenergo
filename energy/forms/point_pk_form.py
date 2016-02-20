# coding:utf8
from django import forms
from energy.models import Point
from energy.models import Period

__author__ = 'Demyanov Kirill'

class PointPKForm(forms.Form):
    point = forms.ModelChoiceField(
        queryset=Point.objects.all(),
    )
    period = forms.ModelChoiceField(
        queryset=Period.objects.all(),
    )
