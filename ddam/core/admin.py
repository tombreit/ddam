from django.contrib import admin
from django.utils.html import format_html

from .models import Asset, Licence, UsageRestriction, Usage


@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(UsageRestriction)
class UsageRestrictionAdmin(admin.ModelAdmin):
    pass


@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "url"]
    search_fields = ["name", "slug", "url"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    readonly_fields = ["image_preview"]

    list_filter = [
        "licence",
    ]

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        list_display.append("image_preview")
        return list_display
    
    def image_preview(self, obj):
        return format_html('<img src="{url}" height={height}>',
            url=obj.file.url,
            height=80,
        )