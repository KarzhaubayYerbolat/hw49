from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser, Team
from django.utils.translation import gettext_lazy as _
from django_admin_relation_links import AdminChangeLinksMixin


class CustomUserAdmin(UserAdmin):
    model = AppUser
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'phone', 'photo', 'team', 'job_title')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ('username', 'email', 'phone', 'team', 'job_title')
    change_links = ['team']


class TeamAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ('title', 'team_lead_link')
    change_links = ['team_lead']


admin.site.register(Team, TeamAdmin)
admin.site.register(AppUser, CustomUserAdmin)
