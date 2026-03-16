"""
Serializers for the News API.

This module provides REST API serialization for Article, Newsletter, Publisher,
and User models, enabling JSON encoding/decoding for API endpoints.
"""
from rest_framework import serializers
from .models import Article, Newsletter, Publisher
from accounts.models import CustomUser


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article model with publisher and journalist information."""
    publisher_name = serializers.CharField(source="publisher.name", read_only=True)
    journalist_username = serializers.CharField(source="journalist.username", read_only=True)

    class Meta:
        model = Article
        fields = ["id","title","content","publisher","publisher_name","journalist","journalist_username","approved","created_at"]


class NewsletterSerializer(serializers.ModelSerializer):
    """Serializer for Newsletter model with related articles and personnel information."""
    journalist_username = serializers.CharField(source="journalist.username", read_only=True)
    publisher_name = serializers.CharField(source="publisher.name", read_only=True)
    articles = ArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Newsletter
        fields = ["id", "title", "description", "journalist", "journalist_username", "publisher", "publisher_name", "articles", "approved", "approved_by", "created_at"]


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for Publisher model with associated editors and journalists."""
    editors = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')
    journalists = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = Publisher
        fields = ["id", "name", "editors", "journalists"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model with basic user information."""
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role"]
