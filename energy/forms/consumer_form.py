# coding:utf8
from django import forms
from energy.models import Consumer

__author__ = 'Demyanov Kirill'


class ConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        exclude = ()
        widgets = {
            'ls': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'production_area': forms.Select(attrs={'class': 'form-control'}),
        }