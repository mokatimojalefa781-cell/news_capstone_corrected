from rest_framework import serializers
from news.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    journalist_username = serializers.CharField(source='journalist.username', read_only=True)
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'journalist',
            'journalist_username',
            'publisher',
            'publisher_name',
            'is_approved',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['is_approved', 'created_at', 'updated_at', 'journalist_username', 'publisher_name']

