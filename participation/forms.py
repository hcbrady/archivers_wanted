from django import forms
from .models import Opportunity, Tag
from ckeditor.widgets import CKEditorWidget 

class OpportunityForm(forms.ModelForm):
    summary = forms.CharField(widget=CKEditorWidget())
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'multiple': 'multiple'  # <-- Ensure this is set
        }),
        required=False
    )
    class Meta:
        model = Opportunity
        fields = ['title', 'summary', 'tags']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
