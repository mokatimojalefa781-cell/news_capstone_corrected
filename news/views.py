"""
Views for the News Application.

This module provides views for managing articles, newsletters, publishers,
and subscriptions with role-based access control (reader, journalist, editor).
"""

import requests

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .decorators import editor_required, journalist_required, reader_required
from .forms import (
    ArticleForm,
    AssignArticleForm,
    NewsletterForm,
    PublisherForm,
)
from .models import (
    Article,
    ArticleSubscription,
    Newsletter,
    Publisher,
)


# ------------------- HOME -------------------
def home(request):
    """
    Public landing page. If user is authenticated, redirect to their dashboard.
    """
    if request.user.is_authenticated:
        return redirect("role_redirect")
    return render(request, "news/home.html")


def register(request):
    """
    Deprecated register view. Use accounts app registration instead.
    """
    return render(request, "registration/register.html")


# ------------------- ROLE REDIRECT -------------------
@login_required
def role_redirect(request):
    """
    Redirect authenticated users to their role-specific dashboard.
    """
    if request.user.role == "reader":
        return redirect("reader_dashboard")
    if request.user.role == "journalist":
        return redirect("journalist_dashboard")
    if request.user.role == "editor":
        return redirect("editor_dashboard")
    return redirect("home")


# ------------------- DASHBOARDS -------------------
@login_required
@reader_required
def reader_dashboard(request):
    articles = Article.objects.filter(approved=True)
    subscribed_articles = Article.objects.filter(
        approved=True,
        pk__in=ArticleSubscription.objects.filter(
            reader=request.user
        ).values_list("article_id", flat=True),
    )
    publisher_articles = Article.objects.filter(
        approved=True,
        publisher__in=request.user.reader_subscriptions.all(),
    )
    journalist_articles = Article.objects.filter(
        approved=True,
        journalist__in=request.user.journalist_subscriptions.all(),
    )

    subscription_feed = (
        (subscribed_articles | publisher_articles | journalist_articles)
        .distinct()
        .order_by("-created_at")
    )

    subscribed_article_ids = set(
        ArticleSubscription.objects.filter(reader=request.user).values_list(
            "article_id", flat=True
        )
    )
    return render(
        request,
        "news/reader_dashboard.html",
        {
            "articles": articles,
            "subscription_feed": subscription_feed,
            "subscribed_article_ids": subscribed_article_ids,
        },
    )


@login_required
def article_list(request):
    """
    Display a list of articles based on user role.

    Readers see only approved articles, while editors and journalists see all.
    """
    if request.user.role == "reader":
        articles = Article.objects.filter(approved=True)
        subscribed_article_ids = set(
            ArticleSubscription.objects.filter(
                reader=request.user
            ).values_list("article_id", flat=True)
        )
    else:
        articles = Article.objects.all()
        subscribed_article_ids = []

    context = {
        "articles": articles,
        "user_role": request.user.role,
        "subscribed_article_ids": subscribed_article_ids,
    }
    return render(request, "news/article_list.html", context)


@login_required
def create_article(request):
    """
    Create a new article.

    Journalists create articles assigned to themselves. Editors can create articles
    assigned to any journalist or leave unassigned.
    """
    if request.method == "POST":
        form = ArticleForm(request.POST, user=request.user)
        if form.is_valid():
            article = form.save(commit=False)
            article.journalist = (
                request.user if request.user.role == "journalist" else None
            )
            article.save()
            messages.success(request, "Article created successfully.")
            return redirect("article_list")
    else:
        form = ArticleForm(user=request.user)
    return render(
        request,
        "news/create_article.html",
        {"form": form, "type": "Create New Article"},
    )


@login_required
def view_article(request, pk):
    """
    Display a single article with permission checks.

    Editors can view any article. Journalists can view approved articles or their own drafts.
    Readers can only view approved articles.
    """
    article = get_object_or_404(Article, pk=pk)
    # Editors can view any article, journalists can view any approved article or their own drafts
    if request.user.role == "editor":
        pass  # Editors can view any article
    elif request.user.role == "journalist":
        if not article.approved and article.journalist != request.user:
            messages.error(
                request, "You can only view your own pending articles."
            )
            return redirect("article_list")
    else:
        # Readers can only view approved articles
        if not article.approved:
            messages.error(request, "This article is not yet approved.")
            return redirect("article_list")
    return render(request, "news/view_article.html", {"article": article})


@login_required
def edit_article(request, pk):
    """
    Edit an existing article.

    Editors can edit any article. Journalists can only edit their own articles.
    """
    article = get_object_or_404(Article, pk=pk)

    # Check permissions
    if request.user.role == "editor":
        pass  # Editors can edit any article
    elif request.user.role == "journalist":
        if article.journalist != request.user:
            messages.error(request, "You can only edit your own articles.")
            return redirect("article_list")
    else:
        messages.error(request, "You don't have permission to edit articles.")
        return redirect("article_list")

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully.")
            return redirect("article_list")
    else:
        form = ArticleForm(instance=article, user=request.user)
    return render(
        request,
        "news/edit_article.html",
        {
            "form": form,
            "title": "Edit Article",
            "submit_label": "Save Changes",
        },
    )


@login_required
def delete_article(request, pk):
    """
    Delete an article.

    Editors can delete any article. Journalists can only delete their own articles.
    """
    article = get_object_or_404(Article, pk=pk)

    # Check permissions
    if request.user.role == "editor":
        pass  # Editors can delete any article
    elif request.user.role == "journalist":
        if article.journalist != request.user:
            messages.error(request, "You can only delete your own articles.")
            return redirect("article_list")
    else:
        messages.error(
            request, "You don't have permission to delete articles."
        )
        return redirect("article_list")

    article.delete()
    messages.success(request, "Article deleted.")
    return redirect("article_list")


# ------------------- JOURNALIST DASHBOARD -------------------
@login_required
@journalist_required
def journalist_dashboard(request):
    """
    Display journalist dashboard with their articles and newsletters.
    """
    articles = Article.objects.filter(journalist=request.user)
    newsletters = Newsletter.objects.filter(journalist=request.user)
    return render(
        request,
        "news/journalist_dashboard.html",
        {"articles": articles, "newsletters": newsletters},
    )


# ------------------- EDITOR DASHBOARD -------------------
@login_required
@editor_required
def editor_dashboard(request):
    """
    Display editor dashboard with articles and newsletters pending approval.
    """
    pending_articles = Article.objects.filter(approved=False)
    approved_articles = Article.objects.filter(approved=True)
    pending_newsletters = Newsletter.objects.filter(approved=False)
    approved_newsletters = Newsletter.objects.filter(approved=True)
    return render(
        request,
        "news/editor_dashboard.html",
        {
            "pending_articles": pending_articles,
            "approved_articles": approved_articles,
            "pending_newsletters": pending_newsletters,
            "approved_newsletters": approved_newsletters,
        },
    )


# ------------------- ARTICLE SUBSCRIPTIONS -------------------
@login_required
@reader_required
def toggle_article_subscription(request, pk):
    """Toggle reader subscription to a given article.

    If the user is already subscribed to the article, unsubscribe them.
    Otherwise, create a new subscription.
    """

    article = get_object_or_404(Article, pk=pk)
    subscription, created = ArticleSubscription.objects.get_or_create(
        reader=request.user,
        article=article,
    )

    if not created:
        subscription.delete()
        messages.success(request, f"Unsubscribed from '{article.title}'.")
    else:
        messages.success(request, f"Subscribed to '{article.title}'.")

    return redirect(request.META.get("HTTP_REFERER", "article_list"))


# ------------------- PUBLISHERS -------------------
@login_required
def publisher_list(request):
    """
    Display list of all publishers.
    """
    publishers = Publisher.objects.all()
    return render(
        request, "news/publisher_list.html", {"publishers": publishers}
    )


@login_required
@editor_required
def create_publisher(request):
    """
    Create a new publisher. Only editors can perform this action.
    """
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            publisher.editors.add(request.user)
            messages.success(request, "Publisher created successfully.")
            return redirect("publisher_list")
    else:
        form = PublisherForm()

    return render(request, "news/create_publisher.html", {"form": form})


@login_required
@editor_required
def edit_publisher(request, pk):
    """
    Edit an existing publisher. Only editors can perform this action.
    """
    publisher = get_object_or_404(Publisher, pk=pk)
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            messages.success(request, "Publisher updated successfully.")
            return redirect("publisher_list")
    else:
        form = PublisherForm(instance=publisher)

    return render(
        request,
        "news/edit_publisher.html",
        {"form": form, "publisher": publisher},
    )


# ------------------- ARTICLE APPROVAL -------------------
@login_required
@editor_required
def approve_article(request, pk):
    """
    Approve a pending article and send notifications to subscribers.
    """
    article = get_object_or_404(Article, pk=pk)
    if not article.approved:
        article.approved = True
        article.approved_by = request.user
        article.save()

        # Send emails to subscribers
        subscribers = []
        if article.publisher:
            subscribers.extend(article.publisher.subscribed_readers.all())
        if article.journalist:
            subscribers.extend(article.journalist.journalist_subscribers.all())

        from django.core.mail import send_mail
        from django.conf import settings

        for subscriber in set(subscribers):  # Remove duplicates
            send_mail(
                f"New Article Approved: {article.title}",
                f"Check out the new article: {article.title}\n\n{article.content[:200]}...",
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email],
                fail_silently=True,
            )

        # POST to /api/approved/ (optional integration)
        try:
            url = (
                "http://localhost:8000/api/approved/"  # Adjust for production
            )
            data = {
                "article_id": article.id,
                "title": article.title,
                "approved_by": request.user.username,
            }
            requests.post(url, json=data, timeout=5)
        except requests.RequestException:
            # If the external endpoint is not available, do not interrupt approval flow.
            pass

        messages.success(request, f"Article '{article.title}' approved.")
    else:
        messages.info(
            request, f"Article '{article.title}' is already approved."
        )
    return redirect("editor_dashboard")


@login_required
@editor_required
def unapprove_article(request, pk):
    """
    Unapprove an approved article, making it unavailable to readers.
    """
    article = get_object_or_404(Article, pk=pk)
    article.approved = False
    article.approved_by = None
    article.save()
    messages.success(request, f"Article '{article.title}' unapproved.")
    return redirect("editor_dashboard")


@login_required
@editor_required
def approve_newsletter(request, pk):
    """
    Approve a pending newsletter.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if not newsletter.approved:
        newsletter.approved = True
        newsletter.approved_by = request.user
        newsletter.save()
        messages.success(request, f"Newsletter '{newsletter.title}' approved.")
    else:
        messages.info(
            request, f"Newsletter '{newsletter.title}' is already approved."
        )
    return redirect("editor_dashboard")


@login_required
@editor_required
def unapprove_newsletter(request, pk):
    """
    Unapprove an approved newsletter.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.approved = False
    newsletter.approved_by = None
    newsletter.save()
    messages.success(request, f"Newsletter '{newsletter.title}' unapproved.")
    return redirect("editor_dashboard")


@login_required
@editor_required
def pending_articles(request):
    """
    View only pending articles for editors.
    """
    pending_articles = Article.objects.filter(approved=False)
    return render(
        request,
        "news/pending_articles.html",
        {"pending_articles": pending_articles},
    )


# ------------------- ASSIGN ARTICLE -------------------
@login_required
@editor_required
def assign_article(request, pk):
    """
    Assign an article to a journalist and publisher. Only editors can perform this action.
    """
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = AssignArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Article '{article.title}' assigned successfully."
            )
            return redirect("editor_dashboard")
    else:
        form = AssignArticleForm(instance=article)

    return render(
        request, "news/assign_article.html", {"form": form, "article": article}
    )


# ------------------- NEWSLETTERS -------------------


@login_required
def newsletter_list(request):
    """
    List newsletters for the logged-in journalist, all for editors, approved for readers.
    """
    if request.user.role == "journalist":
        newsletters = Newsletter.objects.filter(journalist=request.user)
    elif request.user.role == "editor":
        newsletters = Newsletter.objects.all()
    else:  # readers
        newsletters = Newsletter.objects.filter(approved=True)
    return render(
        request, "news/newsletter_list.html", {"newsletters": newsletters}
    )


@login_required
@journalist_required
def create_newsletter(request):
    """
    Allow a journalist to create a newsletter (article linked to publisher).
    """
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.journalist = request.user
            newsletter.save()
            messages.success(request, "Newsletter created successfully.")
            return redirect("newsletter_list")
    else:
        form = NewsletterForm()
    return render(
        request,
        "news/create_newsletter.html",
        {
            "form": form,
            "title": "Create New Newsletter",
            "submit_label": "Save Newsletter",
        },
    )


@login_required
def view_newsletter(request, pk):
    """
    View a single newsletter by its primary key.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)
    # Editors can view any newsletter, journalists can view any approved newsletter or their own drafts
    if request.user.role == "editor":
        pass  # Editors can view any newsletter
    elif request.user.role == "journalist":
        if not newsletter.approved and newsletter.journalist != request.user:
            messages.error(
                request, "You can only view your own pending newsletters."
            )
            return redirect("newsletter_list")
    else:
        # Readers can only view approved newsletters
        if not newsletter.approved:
            messages.error(request, "This newsletter is not yet approved.")
            return redirect("newsletter_list")
    return render(
        request, "news/view_newsletter.html", {"newsletter": newsletter}
    )


@login_required
def edit_newsletter(request, pk):
    """
    Edit a newsletter (journalists their own, editors any).
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)

    # Check permissions
    if request.user.role == "editor":
        pass  # Editors can edit any newsletter
    elif request.user.role == "journalist":
        if newsletter.journalist != request.user:
            messages.error(request, "You can only edit your own newsletters.")
            return redirect("newsletter_list")
    else:
        messages.error(
            request, "You don't have permission to edit newsletters."
        )
        return redirect("newsletter_list")

    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated successfully.")
            return redirect("newsletter_list")
    else:
        form = NewsletterForm(instance=newsletter)

    return render(
        request,
        "news/edit_newsletter.html",
        {
            "form": form,
            "title": "Edit Newsletter",
            "submit_label": "Save Changes",
        },
    )


@login_required
def delete_newsletter(request, pk):
    """
    Delete a newsletter (journalists their own, editors any).
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)

    # Check permissions
    if request.user.role == "editor":
        pass  # Editors can delete any newsletter
    elif request.user.role == "journalist":
        if newsletter.journalist != request.user:
            messages.error(
                request, "You can only delete your own newsletters."
            )
            return redirect("newsletter_list")
    else:
        messages.error(
            request, "You don't have permission to delete newsletters."
        )
        return redirect("newsletter_list")

    newsletter.delete()
    messages.success(request, "Newsletter deleted successfully.")
    return redirect("newsletter_list")


def view_publisher(request, pk):
    """
    Display a publisher profile with their approved articles and newsletters.
    """
    publisher = get_object_or_404(Publisher, pk=pk)

    articles = publisher.articles.filter(approved=True)
    newsletters = publisher.newsletters.filter(approved=True)

    context = {
        "publisher": publisher,
        "articles": articles,
        "newsletters": newsletters,
    }

    return render(request, "news/view_publisher.html", context)


# ------------------- SUBSCRIPTIONS -------------------
@login_required
@reader_required
def subscribe_publishers(request):
    if request.method == "POST":
        publisher_id = request.POST.get("publisher_id")
        action = request.POST.get("action")
        publisher = get_object_or_404(Publisher, pk=publisher_id)

        if action == "subscribe":
            request.user.reader_subscriptions.add(publisher)
            messages.success(request, f"Subscribed to {publisher.name}.")
        elif action == "unsubscribe":
            request.user.reader_subscriptions.remove(publisher)
            messages.success(request, f"Unsubscribed from {publisher.name}.")

        return redirect("subscribe_publishers")

    publishers = Publisher.objects.all()
    return render(
        request, "news/subscribe_publishers.html", {"publishers": publishers}
    )


@login_required
@reader_required
def subscribe_journalists(request):
    if request.method == "POST":
        journalist_id = request.POST.get("journalist_id")
        action = request.POST.get("action")
        journalist = get_object_or_404(
            get_user_model(), pk=journalist_id, role="journalist"
        )

        if action == "subscribe":
            request.user.journalist_subscriptions.add(journalist)
            messages.success(request, f"Subscribed to {journalist.username}.")
        elif action == "unsubscribe":
            request.user.journalist_subscriptions.remove(journalist)
            messages.success(
                request, f"Unsubscribed from {journalist.username}."
            )

        return redirect("subscribe_journalists")

    journalists = get_user_model().objects.filter(role="journalist")
    user_subscriptions = request.user.journalist_subscriptions.values_list(
        "id", flat=True
    )
    return render(
        request,
        "news/subscribe_journalists.html",
        {"journalists": journalists, "user_subscriptions": user_subscriptions},
    )
