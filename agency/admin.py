from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from agency.models import Topic, Newspaper, Redactor


# Register your models here.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "topic", "published_date")
    search_fields = ("title", "topic__name")
    list_filter = ("topic", "published_date")


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    model = Redactor
    list_display = ("username", "first_name", "last_name", "email", "years_of_experience", "is_staff")
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("years_of_experience",)}),
    )
