from django import forms
from .models import Article, Newsletter, Publisher
from accounts.models import CustomUser


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your article content here...',
                'rows': 6
            }),
            'publisher': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter newsletter title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your newsletter content here...',
                'rows': 6
            }),
            'publisher': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class JournalistSubscriptionForm(forms.Form):
    journalists = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='journalist'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Subscribe to Journalists"
    )


class PublisherSubscriptionForm(forms.Form):
    publishers = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Subscribe to Publishers"
    )

