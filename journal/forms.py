from journal.models import Message

__author__ = 'Demyanov Kirill'

from django import forms

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['number', 'description']
