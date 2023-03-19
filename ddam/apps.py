from django.contrib.admin.apps import AdminConfig


class DDAMAdminConfig(AdminConfig):
    default_site = 'ddam.admin.DDAMAdminSite'
