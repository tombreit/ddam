from django import forms
from django.db.models import Count, Q

import django_filters

from .models import Asset, License, Usage
from .forms import AssetFilterForm


class AssetFilter(django_filters.FilterSet):

    def custom_string_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        )

    title = django_filters.CharFilter(
        method='custom_string_search',
        label="Search",
    )
    usage = django_filters.ModelMultipleChoiceFilter(
        field_name='usage',
        # field_name='usage__slug',
        # to_field_name='slug',
        # conjoined=True,  # AND conjunction
        widget=forms.CheckboxSelectMultiple,
        queryset=(
            Usage
            .objects
            .annotate(
                count=Count('asset'),
            )
            # .exclude(count=0)
        )
    )
    license = django_filters.ModelChoiceFilter(
        field_name='license',
        # field_name='license__slug',
        # to_field_name='slug',
        null_label='No license',
        widget=forms.RadioSelect,
        queryset=(
            License
            .objects
            .annotate(
                count=Count('asset'),
            )
        )
    )

    class Meta:
        model = Asset
        form = AssetFilterForm
        fields = [
            'dealer',
            'with_costs',
        ]
