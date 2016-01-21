# coding:utf8
from django import forms

__author__ = 'Demyanov Kirill'

class PointPKForm(forms.Form):
    point = forms.IntegerField()
    period = forms.IntegerField()
