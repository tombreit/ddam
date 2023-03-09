from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='core/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('ddam.accounts.urls')),
    path('core/', include('ddam.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
