from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    path('', views.asset_filter_list, name="asset-list"),
    path('upload/', views.MultiFileFieldFormView.as_view(), name='asset-upload-multiple'),
    path('create/', views.AssetCreate.as_view(), name='asset-create'),
    path('<uuid:id>/', views.AssetDetailView.as_view(), name='asset-detail'),
    path('<uuid:id>/update/', views.AssetUpdate.as_view(), name='asset-update'),

    path('usage/', views.UsageListView.as_view(), name="usage-list"),
    path('usage/create/', views.UsageCreateView.as_view(), name='usage-create'),
    path('usage/<uuid:id>/update/', views.UsageUpdateView.as_view(), name='usage-update'),

    path('license/', views.LicenseListView.as_view(), name="license-list"),
    path('license/create/', views.LicenseCreate.as_view(), name='license-create'),
    path('license/<uuid:id>/update/', views.LicenseUpdate.as_view(), name='license-update'),

    path('dealer/', views.DealerListView.as_view(), name="dealer-list"),
    path('dealer/create/', views.DealerCreate.as_view(), name='dealer-create'),
    path('dealer/<uuid:id>/update/', views.DealerUpdate.as_view(), name='dealer-update'),
]
