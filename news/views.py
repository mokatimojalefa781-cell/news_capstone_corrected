from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Newsletter, Publisher

# ------------------- HOME -------------------
def home(request):
    return render(request, "news/home.html")

# ------------------- ARTICLES -------------------
@login_required
def article_list(request):
    articles = Article.objects.all()
    return render(request, "news/article_list.html", {"articles": articles})

@login_required
def create_article(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Article.objects.create(title=title, content=content)
        messages.success(request, "Article created successfully.")
        return redirect("article_list")
    return render(request, "news/create_article.html")

@login_required
def view_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "news/view_article.html", {"article": article})

@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.save()
        messages.success(request, "Article updated successfully.")
        return redirect("view_article", pk=article.pk)
    return render(request, "news/edit_article.html", {"article": article})

@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    messages.success(request, "Article deleted successfully.")
    return redirect("article_list")

# ------------------- NEWSLETTERS -------------------
@login_required
def newsletter_list(request):
    newsletters = Newsletter.objects.all()
    return render(request, "news/newsletter_list.html", {"newsletters": newsletters})

@login_required
def create_newsletter(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        Newsletter.objects.create(title=title, content=content)
        messages.success(request, "Newsletter created successfully.")
        return redirect("newsletter_list")
    return render(request, "news/create_newsletter.html")

@login_required
def view_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, "news/view_newsletter.html", {"newsletter": newsletter})

@login_required
def edit_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == "POST":
        newsletter.title = request.POST.get("title")
        newsletter.content = request.POST.get("content")
        newsletter.save()
        messages.success(request, "Newsletter updated successfully.")
        return redirect("view_newsletter", pk=newsletter.pk)
    return render(request, "news/edit_newsletter.html", {"newsletter": newsletter})

@login_required
def delete_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.delete()
    messages.success(request, "Newsletter deleted successfully.")
    return redirect("newsletter_list")

# ------------------- DASHBOARD -------------------
@login_required
def journalist_dashboard(request):
    return render(request, "news/journalist_dashboard.html")

@login_required
def pending_articles(request):
    return render(request, "news/pending.html")

# ------------------- SUBSCRIPTIONS -------------------
@login_required
def subscribe_publishers(request):
    return render(request, "news/subscribe_publishers.html")

@login_required
def subscribe_journalists(request):
    return render(request, "news/subscribe_journalists.html")

# ------------------- PUBLISHER LIST -------------------
@login_required
def publisher_list(request):
    publishers = Publisher.objects.all()
    return render(request, "news/publisher_list.html", {"publishers": publishers})

# ------------------- ROLE REDIRECT -------------------
@login_required
def role_redirect(request):
    if hasattr(request.user, "role"):
        if request.user.role == "journalist":
            return redirect("journalist_dashboard")
        elif request.user.role == "editor":
            return redirect("pending_articles")
    return redirect("home")










