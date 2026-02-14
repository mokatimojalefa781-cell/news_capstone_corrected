from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Articles
    path("articles/", views.article_list, name="article_list"),
    path("articles/create/", views.create_article, name="create_article"),
    path("articles/view/<int:pk>/", views.view_article, name="view_article"),
    path("articles/edit/<int:pk>/", views.edit_article, name="edit_article"),
    path("articles/delete/<int:pk>/", views.delete_article, name="delete_article"),

    # Newsletters
    path("newsletters/", views.newsletter_list, name="newsletter_list"),
    path("newsletters/create/", views.create_newsletter, name="create_newsletter"),
    path("newsletters/view/<int:pk>/", views.view_newsletter, name="view_newsletter"),
    path("newsletters/edit/<int:pk>/", views.edit_newsletter, name="edit_newsletter"),
    path("newsletters/delete/<int:pk>/", views.delete_newsletter, name="delete_newsletter"),

    # Journalist Dashboard
    path("dashboard/", views.journalist_dashboard, name="journalist_dashboard"),

    # Pending/Approval
    path("pending/", views.pending_articles, name="pending_articles"),

    # Subscription management
    path("subscribe/publishers/", views.subscribe_publishers, name="subscribe_publishers"),
    path("subscribe/journalists/", views.subscribe_journalists, name="subscribe_journalists"),

    # Publisher list
    path("publishers/", views.publisher_list, name="publisher_list"),

    # Role-based redirect
    path("redirect/", views.role_redirect, name="role_redirect"),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]










