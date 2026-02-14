from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer

class ReaderSubscribedArticlesAPIView(APIView):
    """
    API endpoint to get all approved articles for a reader
    based on their subscribed publishers.
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
            Article.objects.filter(is_approved=True, publisher__in=user.reader_subscriptions.all())
            .select_related("publisher", "journalist")
            .distinct()
            .order_by("-created_at")
        )

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

