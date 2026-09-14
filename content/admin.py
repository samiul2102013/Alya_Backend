from django.contrib import admin

from .models import Category, Consultation, Emirate, FooterContent, Initiative, NewsArticle, Short


@admin.register(Short)
class ShortAdmin(admin.ModelAdmin):
    list_display = ('video_title', 'category', 'status', 'published_at')
    search_fields = ('video_title', 'organization')
    list_filter = ('status', 'category')


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'category', 'status', 'published_date')
    search_fields = ('article_title',)
    list_filter = ('status', 'category')


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'emirates', 'status')
    search_fields = ('title',)
    list_filter = ('status', 'category')


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('session_title', 'session_type', 'status', 'date')
    search_fields = ('session_title',)
    list_filter = ('status', 'session_type')


@admin.register(Emirate)
class EmirateAdmin(admin.ModelAdmin):
    list_display = ('emirates_name', 'status')
    search_fields = ('emirates_name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    search_fields = ('name',)


@admin.register(FooterContent)
class FooterContentAdmin(admin.ModelAdmin):
    list_display = ('brand_text', 'phone', 'email', 'published')

    def has_add_permission(self, request):
        # Singleton: allow add only while no record exists.
        return not FooterContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False