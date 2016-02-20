# coding:utf8
from django import forms
from energy.models import Consumer

__author__ = 'Demyanov Kirill'


class ConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        exclude = ['old_id']
        widgets = {
            'ls': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '100010',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'ИП Иванов В.В.',
                }
            ),
            'inn': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '500100732259',
                }
            ),
            'kpp': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '773301001',
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'production_area': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
