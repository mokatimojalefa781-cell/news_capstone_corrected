from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Articles
    path('', views.home, name='home'),
    path("articles/", views.article_list, name="article_list"),
    path("articles/create/", views.create_article, name="create_article"),
    path("articles/view/<int:pk>/", views.view_article, name="view_article"),
    path("articles/edit/<int:pk>/", views.edit_article, name="edit_article"),
    path("articles/delete/<int:pk>/", views.delete_article, name="delete_article"),
    path("articles/approve/<int:pk>/", views.approve_article, name="approve_article"),
    path("articles/unapprove/<int:pk>/", views.unapprove_article, name="unapprove_article"),
    path("articles/assign/<int:pk>/", views.assign_article, name="assign_article"),
    path("articles/subscribe/<int:pk>/", views.toggle_article_subscription, name="toggle_article_subscription"),

    # Newsletters
    path("newsletters/", views.newsletter_list, name="newsletter_list"),
    path("newsletters/create/", views.create_newsletter, name="create_newsletter"),
    path("newsletters/view/<int:pk>/", views.view_newsletter, name="view_newsletter"),
    path("newsletters/edit/<int:pk>/", views.edit_newsletter, name="edit_newsletter"),
    path("newsletters/delete/<int:pk>/", views.delete_newsletter, name="delete_newsletter"),
    path("newsletters/approve/<int:pk>/", views.approve_newsletter, name="approve_newsletter"),
    path("newsletters/unapprove/<int:pk>/", views.unapprove_newsletter, name="unapprove_newsletter"),

    # Moderation
    path("pending/", views.pending_articles, name="pending_articles"),

    # Subscription management
    path("subscribe/publishers/", views.subscribe_publishers, name="subscribe_publishers"),
    path("subscribe/journalists/", views.subscribe_journalists, name="subscribe_journalists"),
    path("reader/dashboard/", views.reader_dashboard, name="reader_dashboard"),
    path("journalist/dashboard/", views.journalist_dashboard, name="journalist_dashboard"),
    path("editor/dashboard/", views.editor_dashboard, name="editor_dashboard"),
    path("role-redirect/", views.role_redirect, name="role_redirect"),

    # Publishers
    path("publishers/", views.publisher_list, name="publisher_list"),
    path("publishers/create/", views.create_publisher, name="create_publisher"),
    path("publishers/edit/<int:pk>/", views.edit_publisher, name="edit_publisher"),
    path("register/", views.register, name="register"),
    path("publishers/view/<int:pk>/", views.view_publisher, name="view_publisher"),


    # Logout
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]
