from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.contrib import messages

from .image_helpers import delete_rendition
from . import models


@admin.register(models.Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ["title"]
    ordering = ["title"]
    search_fields = ["title"]
    # prepopulated_fields = {"slug": ["title"]}


@admin.register(models.Dealer)
class DealerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ["title", "url"]
    search_fields = ["title", "url"]
    # prepopulated_fields = {"slug": ["title"]}


@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    readonly_fields = [
        "image_preview",
    ]

    list_filter = [
        "license",
    ]

    actions = [
        "delete_renditions",
    ]

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        list_display.append("image_preview")
        return list_display

    def image_preview(self, obj):
        return format_html('<img src="{url}" height={height}>',
            url=obj.file.url,
            height=60,
        )

    @admin.action(description='Purge image renditions')
    def delete_renditions(self, request, queryset):
        deleted = 0

        for obj in queryset:
            deleted_result = delete_rendition(obj.file)
            if deleted_result:
                deleted += 1

        self.message_user(request, ngettext(
            '%d rendition was successfully deleted.',
            '%d renditions were successfully deleted.',
            deleted,
        ) % deleted, messages.SUCCESS)
