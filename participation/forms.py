from django import forms
from .models import Opportunity, Tag
from ckeditor.widgets import CKEditorWidget 

class OpportunityForm(forms.ModelForm):
    summary = forms.CharField(widget=CKEditorWidget())
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'multiple': 'multiple'
        }),
        required=False
    )
    class Meta:
        model = Opportunity
        fields = ['title', 'summary', 'tags', 'defunct']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'category']

class TagSubscriptionForm(forms.Form):
    email = forms.EmailField()
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'multiple': 'multiple'
        }),
        required=False
    )

class RecommendForm(forms.Form):
    title = forms.CharField()
    email = forms.EmailField()
    text = forms.CharField(widget=CKEditorWidget())
