from django import forms
from .models import Opportunity, Tag

class OpportunityForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget = forms.SelectMultiple(attrs={'class': 'form-select'}),
        required = False
    )
    class Meta:
        model = Opportunity
        fields = ['title', 'summary', 'tags']
