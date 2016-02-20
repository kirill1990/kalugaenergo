# coding:utf8
from django import forms
from energy.models import OrumType

__author__ = 'Demyanov Kirill'

class OrumSettingForm(forms.Form):
    orum_type = forms.ModelChoiceField(
        label=u'Тип орума',
        queryset=OrumType.objects.all(),
        empty_label=None,
        # choices=[(orum_type.pk, orum_type) for orum_type in OrumType.objects.all()],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    power = forms.DecimalField(
        label=u'Мощность',
        min_value=0.001,
        max_value=1000,
        decimal_places=3,
        max_digits=14,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '511.001',
            }
        ),
    )
    ratio = forms.DecimalField(
        label=u'Коэффициент',
        min_value=0.001,
        max_value=100,
        decimal_places=3,
        max_digits=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '1.001',
            }
        ),
    )
    hours = forms.IntegerField(
        label=u'Часы',
        min_value=1,
        max_value=1000,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '24',
            }
        ),
    )
