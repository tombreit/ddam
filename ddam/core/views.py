from django.db.models import Count, Case, Value, When
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Asset, License, Usage, Dealer
from .filters import AssetFilter
from .forms import MultiFileFieldForm, AssetForm


@login_required
def asset_filter_list(request):
    queryset = (
        Asset
        .objects
        .select_related("license")
        .order_by("-created_at")
    )
    asset_filter = AssetFilter(request.GET, queryset=queryset)
    return render(request, 'core/asset_filter_list.html', {'filter': asset_filter})


class MultiFileFieldFormView(LoginRequiredMixin, FormView):
    form_class = MultiFileFieldForm
    template_name = 'core/asset_upload_multiple.html'
    success_url = '/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            assets_upload = []

            for f in files:
                print(f"{f=}")  # Do something with each file.
                asset = Asset(
                    file=f,
                    title=f.name,
                    filename_orig=f.name,
                    created_by=request.user.email,
                )
                assets_upload.append(asset)
            
            print(f"{assets_upload=}")
            Asset.objects.bulk_create(assets_upload)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AssetDetailView(LoginRequiredMixin, DetailView):
    model = Asset
    pk_url_kwarg = "id"


class AssetCreate(LoginRequiredMixin, CreateView):
    model = Asset
    pk_url_kwarg = "id"
    form_class = AssetForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user.email
        form.instance.filename_orig = form.cleaned_data['file'].name
        return super().form_valid(form)


class AssetUpdate(LoginRequiredMixin, UpdateView):
    model = Asset
    pk_url_kwarg = "id"
    form_class = AssetForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.email
        return super().form_valid(form)


class BaseListView(LoginRequiredMixin, ListView):
    context_object_name = "objects"
    template_name = "core/related_object_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "model": self.model,
        })
        return context

    def get_queryset(self):

        try:
            to_highlight = self.request.GET.get('highlight')
            to_highlight_id = to_highlight.replace("object-", "")
        except:
            to_highlight_id = None

        queryset = super().get_queryset()
        queryset = (
            queryset
            .annotate(
                count=Count('asset'),
            )
            .annotate(
                highlight=Case(
                    When(id=to_highlight_id, then=Value(1)
                ), default=Value(0))
            )
            .order_by("-count")
        )
        return queryset


class BaseInstanceView:
    pk_url_kwarg = "id"

    def get_success_url(self):
        app_label, model_name = self.model.get_app_label_and_model_name()
        success_url = f"{app_label}:{model_name}-list"
        highlight_query_param = f"highlight=object-{self.object.id}"
        return f"{reverse(success_url)}?{highlight_query_param}"


class UsageListView(BaseListView):
    model = Usage


class UsageCreateView(LoginRequiredMixin, BaseInstanceView, CreateView):
    model = Usage
    fields = [
        "title",
        "media",
        "notes",
    ]


class UsageUpdateView(LoginRequiredMixin, BaseInstanceView, UpdateView):
    model = Usage
    fields = [
        "title",
        "media",
        "notes",
    ]


class LicenseListView(BaseListView):
    model = License


class LicenseCreate(LoginRequiredMixin, BaseInstanceView, CreateView):
    model = License
    fields = '__all__'


class LicenseUpdate(LoginRequiredMixin, BaseInstanceView, UpdateView):
    model = License
    fields = '__all__'


class DealerListView(BaseListView):
    model = Dealer


class DealerCreate(LoginRequiredMixin, BaseInstanceView, CreateView):
    model = Dealer
    fields = '__all__'


class DealerUpdate(LoginRequiredMixin, BaseInstanceView, UpdateView):
    model = Dealer
    fields = '__all__'

