from django.contrib import admin
from .models import Category, Route, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'difficulty', 'distance_km',
        'location', 'is_published', 'created_by', 'created_at'
    )
    list_filter = ('difficulty', 'is_published', 'categories')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories',)
    inlines = [ReviewInline]
    list_editable = ('is_published',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('route', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'route__title')
