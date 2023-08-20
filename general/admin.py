from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from rangefilter.filters import DateRangeFilter
from general.models import (
    User,
    Post,
    Comment,
    Reaction,
)
from django.contrib.auth.models import Group
from general.filters import AuthorFilter, PostFilter
from django_admin_listfilter_dropdown import ChoiceDropdownFilter


admin.site.unregister(Group)


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "date_joined",
    )

    readonly_fields = (
        "date_joined",
        "last_login",
    )

    search_fields = (
        "id",
        "username",
        "email",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        ("date_joined", DateRangeFilter),
    )

    autocomplete_fields = (
        'author',
        'post',
    )

    fieldsets = (
        (
            "Личные данные", {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            }
        ),
        (
            "Учетные данные", {
                "fields": (
                    "username",
                    "password",
                )
            }
        ),
        (
            "Статусы", {
                "classes": (
                    "collapse",
                ),
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            }
        ),
        (
            None, {
                "fields": (
                    "friends",
                )
            }
        ),
        (
            "Даты", {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            }
        )
    )


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "title",
        "get_body",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    search_fields = (
        "id",
        "title",
    )

    autocomplete_fields = (
        'author',
        'title',
    )

    list_filter = (
        ("created_at", DateRangeFilter),
    )

    def get_body(self, obj):
        max_length = 64
        if len(obj.body) > max_length:
            return obj.body[:61] + "..."
        return obj.body
    
    get_body.short_description = "body"

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_queryset(self, request) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related("comments")


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "body",
        "created_at",
    )
    list_display_links = (
        "id",
        "body",
    )

    search_fields = (
        "id",
        "author__username",
        "post__title",
    )

    list_filter = (
        PostFilter,
        AuthorFilter,
    )

    raw_id_fields = (
        "author",
    )


@admin.register(Reaction)
class ReactionModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "value",
    )

    search_fields = (
        "id",
        "author__username",
        "post__author",
    )
    list_filter = (
        PostFilter,
        AuthorFilter,
        ("value", ChoiceDropdownFilter),
    )
