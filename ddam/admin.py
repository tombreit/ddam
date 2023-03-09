from django.conf import settings
from django.contrib import admin


class DDAMAdminSite(admin.AdminSite):
    site_header = "DDAM"
    site_title = "DDAM Portal"
    index_title = "Welcome to the DDAM Portal"
