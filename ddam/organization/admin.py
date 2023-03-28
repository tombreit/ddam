from django.contrib import admin

from .models import Branding


@admin.register(Branding)
class BrandingAdmin(admin.ModelAdmin):
    list_display = ('organization_name_en',)

    fieldsets = (
        (None, {
            'fields': (
                ('organization_name_en', 'organization_name_de'),
                'organization_url', 'organization_abbr',
            )
        }),
        ('Address', {
            'classes': ('collapse',),
            'fields': (
                'organization_street',
                'organization_zip_code',
                'organization_city',
            ),
        }),
        ('Logos', {
            'classes': ('collapse',),
            'fields': (
                'organization_logo',
                'organization_figurative_mark',
                'organization_favicon'
            ),
        }),
        ('Misc', {
            'classes': ('collapse',),
            'fields': (
                'documentation_url',
            ),
        }),
    )

    def has_add_permission(self, request):
        has_add_permisson = super().has_add_permission(request)
        if has_add_permisson and Branding.objects.exists():
            has_add_permisson = False
        return has_add_permisson
