from django import forms
from .models import Publisher


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"


class SearchForm(forms.Form):
    choices = (
        ('title', 'Title'),
        ('contributor', 'Contributor')
    )
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=choices)