"""
Forms used in the News Application.

These forms handle:
- Newsletter creation
- Assigning articles to journalists and publishers
- Reader subscriptions to journalists
- Reader subscriptions to publishers
- Creating and managing publishers
"""

from django import forms
from .models import Article, Publisher, Newsletter
from accounts.models import CustomUser


class NewsletterForm(forms.ModelForm):
    """Form used by journalists to create newsletters."""

    class Meta:
        model = Newsletter
        fields = ["title", "description", "publisher", "articles"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "publisher": forms.Select(attrs={"class": "form-select"}),
            "articles": forms.SelectMultiple(attrs={"class": "form-select"}),
        }


class AssignArticleForm(forms.ModelForm):
    """
    Form used by editors or admins to assign an article
    to a specific journalist and publisher.
    """

    journalist = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role="journalist"),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Article
        fields = ["journalist", "publisher"]
        widgets = {
            "publisher": forms.Select(attrs={"class": "form-select"}),
        }


class JournalistSubscriptionForm(forms.Form):
    """
    Allows readers to subscribe to journalists.
    """

    journalists = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role="journalist"),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=False,
        label="Subscribe to Journalists",
    )


class PublisherSubscriptionForm(forms.Form):
    """
    Allows readers to subscribe to publishers.
    """

    publishers = forms.ModelMultipleChoiceField(
        queryset=Publisher.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        required=False,
        label="Subscribe to Publishers",
    )


class PublisherForm(forms.ModelForm):
    """
    Form used to create or update a publisher and assign journalists to it.
    """

    class Meta:
        model = Publisher
        fields = ["name", "journalists"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Publisher name"}
            ),
            "journalists": forms.SelectMultiple(attrs={"class": "form-select"}),
        }

class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing articles.
    """
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.role == 'journalist':
            # Journalists can't change journalist field
            self.fields.pop('journalist', None)

    class Meta:
        model = Article
        fields = ["title", "content", "publisher", "journalist"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "publisher": forms.Select(attrs={"class": "form-select"}),
            "journalist": forms.Select(attrs={"class": "form-select"}),
        }
