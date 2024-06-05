from django.contrib import admin
from django.utils.html import format_html
from .models import Author, Book, LikeDislike, Review, Category, Cart, Tag

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthdate', 'email')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'like_count', 'dislike_count', 'cover_image', 'banner_image')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    list_filter = ('author',)
    fields = ('title', 'author', 'description', 'price', 'cover', 'banner')
    autocomplete_fields = ('author',)

    def cover_image(self, obj):
        if obj.cover:
            return format_html('<img src="{}" width="50" height="75" />', obj.cover.url)
        return 'No Cover'
    cover_image.short_description = 'Cover'

    def banner_image(self, obj):
        if obj.banner:
            return format_html('<img src="{}" width="100" height="50" />', obj.banner.url)
        return 'No Banner'
    banner_image.short_description = 'Banner'

@admin.register(LikeDislike)
class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'like')
    search_fields = ('book__title', 'user__username')
    list_filter = ('like',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'message', 'created_at')
    search_fields = ('book__title', 'user__username')
    list_filter = ('rating',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity')

@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('category', 'Book')
    search_fields = ('category__name', 'Book__title')
    list_filter = ('category', 'Book')