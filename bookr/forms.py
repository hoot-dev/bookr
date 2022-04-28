from django import forms


class SearchForm(forms.Form):
    choices = (
        ('title','Title'),
        ('contributor', 'Contributor')
    )
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=choices)