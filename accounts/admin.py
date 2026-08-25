from django.contrib import admin

from .models import AdminUser, PrivacyPolicy, Terms


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'username', 'is_admin_user', 'is_active')
    search_fields = ('email', 'name', 'username')


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('updated_at',)


@admin.register(Terms)
class TermsAdmin(admin.ModelAdmin):
    list_display = ('updated_at',)