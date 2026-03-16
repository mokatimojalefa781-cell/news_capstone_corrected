"""
REST API views for the News Application.

This module provides API endpoints for managing articles, including listing,
creating, updating, and deleting with role-based access control.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer

class ReaderSubscribedArticlesAPIView(APIView):
    """
    Returns articles for readers based on their subscribed publishers.
    Only accessible by users with role 'reader'.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != "reader":
            return Response(
                {"detail": "Only readers can use this endpoint."},
                status=403
            )

        # Get all approved articles from publishers the reader is subscribed to
        articles = (
            Article.objects.filter(approved=True, publisher__in=user.reader_subscriptions.all())
            .select_related("publisher", "journalist")
            .distinct()
            .order_by("-created_at")
        )

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class AllApprovedArticlesAPIView(APIView):
    """API endpoint returning all approved articles across publishers."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Readers, journalists, and editors can inspect the public article feed.
        articles = (
            Article.objects.filter(approved=True)
            .select_related("publisher", "journalist")
            .order_by("-created_at")
        )
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleListCreateAPIView(ListCreateAPIView):
    """
    API view for listing and creating articles.
    
    GET: Returns a list of all approved articles.
    POST: Allows authenticated journalists to create new articles.
    """
    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'journalist':
            raise PermissionDenied("Only journalists can create articles.")
        serializer.save(journalist=self.request.user)


class ArticleDetailAPIView(RetrieveAPIView):
    """
    API view for retrieving a single article by its primary key.
    
    GET: Returns the requested approved article.
    """
    queryset = Article.objects.filter(approved=True)
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting articles.
    
    Editors can perform operations on all articles. Journalists can only
    modify their own articles. Readers cannot access this endpoint.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'editor':
            return Article.objects.all()
        elif user.role == 'journalist':
            return Article.objects.filter(journalist=user)
        return Article.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        if user.role not in ['editor', 'journalist']:
            raise PermissionDenied("Only editors and journalists can update articles.")
        if user.role == 'journalist' and serializer.instance.journalist != user:
            raise PermissionDenied("You can only update your own articles.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role not in ['editor', 'journalist']:
            raise PermissionDenied("Only editors and journalists can delete articles.")
        if user.role == 'journalist' and instance.journalist != user:
            raise PermissionDenied("You can only delete your own articles.")
        instance.delete()


class ApprovedArticleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # This endpoint logs approved articles
        # In a real app, this could save to a log or external service
        data = request.data
        # For now, just return success
        return Response({"message": "Article approval logged", "data": data}, status=status.HTTP_200_OK)


