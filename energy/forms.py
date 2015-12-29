from django import forms
from energy.models import Consumer


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


class PointForm(forms.Form):
    orum = forms.IntegerField()
    period = forms.IntegerField()
    date_use = forms.IntegerField(min_value=0, max_value=1000)
