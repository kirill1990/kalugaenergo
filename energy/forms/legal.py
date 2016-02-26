# coding:utf8
from django import forms
from energy.models import Legal

__author__ = 'Demyanov Kirill'


class LegalForm(forms.ModelForm):
    class Meta:
        model = Legal
        exclude = ['old_id']
        widgets = {
            'ls': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '100125',
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
            'production_area': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
