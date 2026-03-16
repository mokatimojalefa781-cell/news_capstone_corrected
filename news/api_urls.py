from django.urls import path
from .api_views import (
    AllApprovedArticlesAPIView,
    ReaderSubscribedArticlesAPIView,
    ArticleDetailAPIView,
    ArticleListCreateAPIView,
    ArticleUpdateDeleteAPIView,
    ApprovedArticleAPIView,
)

app_name = "news_api"

urlpatterns = [
    path("articles/", ArticleListCreateAPIView.as_view(), name="article_list_create"),
    path("articles/<int:pk>/", ArticleDetailAPIView.as_view(), name="article_detail"),
    path("articles/<int:pk>/update/", ArticleUpdateDeleteAPIView.as_view(), name="article_update_delete"),
    path("all-articles/", AllApprovedArticlesAPIView.as_view(), name="all_articles"),
    path("subscribed-articles/", ReaderSubscribedArticlesAPIView.as_view(), name="reader_articles"),
    path("approved/", ApprovedArticleAPIView.as_view(), name="approved"),
]
