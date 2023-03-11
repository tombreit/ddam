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
    path('usage/<int:pk>/', views.UsageDetailView.as_view(), name='usage-detail'),
    path('usage/<int:pk>/update/', views.UsageUpdateView.as_view(), name='usage-update'),

    path('licence/', views.LicenceListView.as_view(), name="licence-list"),
    path('licence/create/', views.LicenceCreate.as_view(), name='licence-create'),
    path('licence/<int:pk>/', views.LicenceDetailView.as_view(), name='licence-detail'),
    path('licence/<int:pk>/update/', views.LicenceUpdate.as_view(), name='licence-update'),

    path('dealer/', views.DealerListView.as_view(), name="dealer-list"),
    path('dealer/create/', views.DealerCreate.as_view(), name='dealer-create'),
    path('dealer/<int:pk>/update/', views.DealerUpdate.as_view(), name='dealer-update'),
]
