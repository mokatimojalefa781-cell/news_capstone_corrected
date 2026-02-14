from django.contrib import admin
from .models import Article, Newsletter, Publisher

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("editors", "journalists")
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "journalist", "publisher", "is_approved", "approved_by", "created_at")
    list_filter = ("is_approved", "publisher")
    search_fields = ("title", "content")
    raw_id_fields = ("journalist", "approved_by", "publisher")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("title", "journalist", "publisher", "is_approved", "created_at")
    list_filter = ("is_approved", "publisher")
    search_fields = ("title", "content")
    raw_id_fields = ("journalist", "publisher")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)



