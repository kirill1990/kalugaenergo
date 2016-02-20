# coding:utf8
from django import forms

__author__ = 'Demyanov Kirill'


class PointForm(forms.Form):
    title = forms.CharField(
        label=u'Наименование точки учета',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'гараж / палатка / баня',
            }
        ),
    )
