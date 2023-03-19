from django.db.models import Count, Q
from django.db.models import Case, Value, When
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Asset, Licence, Usage, Dealer
from .filters import AssetFilter
from .forms import MultiFileFieldForm, AssetForm


@login_required
def asset_filter_list(request):
    queryset = (
        Asset
        .objects
        .select_related("licence")
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


class UsageListView(LoginRequiredMixin, ListView):
    model = Usage
    context_object_name = "usage"
    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = (
            queryset
            .annotate(
                count=Count('asset'),
            )
            .order_by("-count")
        )

        return queryset


class UsageDetailView(LoginRequiredMixin, DetailView):
    model = Usage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Asset.objects.filter(usage=self.kwargs['pk']).count()
        return context


class UsageCreateView(LoginRequiredMixin, CreateView):
    model = Usage
    fields = [
        "name",
        "media",
        "notes",
    ]


class UsageUpdateView(LoginRequiredMixin, UpdateView):
    model = Usage
    fields = [
        "name",
        "media",
        "notes",
    ]


class LicenceListView(LoginRequiredMixin, ListView):
    model = Licence
    context_object_name = "licences"

    def get_queryset(self):
        qs = (
            Licence
            .objects
            .annotate(
                count=Count('asset'),
            )
            .all()
        )
        return qs


class LicenceDetailView(LoginRequiredMixin, DetailView):
    model = Licence

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Asset.objects.filter(licence=self.kwargs['pk']).count()
        return context


class LicenceCreate(LoginRequiredMixin, CreateView):
    model = Licence
    fields = '__all__'


class LicenceUpdate(LoginRequiredMixin, UpdateView):
    model = Licence
    fields = '__all__'


class DealerListView(LoginRequiredMixin, ListView):
    model = Dealer
    context_object_name = "dealers"

    def get_queryset(self):
        try:
            to_highlight = self.request.GET.get('highlight')
            to_highlight_dealer_id = to_highlight.replace("dealer-", "")
        except:
            to_highlight_dealer_id = None

        qs = (
            Dealer
            .objects
            .annotate(
                count=Count('asset'),
            )
            .annotate(
                highlight=Case(
                    When(id=to_highlight_dealer_id, then=Value(1)
                ), default=Value(0))
            )
            .all()
            .order_by("name")
        )
        return qs


class DealerCreate(LoginRequiredMixin, CreateView):
    model = Dealer
    fields = '__all__'

    def get_success_url(self):
        return f"{reverse('core:dealer-list')}?highlight=dealer-{self.object.id}"


class DealerUpdate(LoginRequiredMixin, UpdateView):
    model = Dealer
    fields = '__all__'

    def get_success_url(self):
        return f"{reverse('core:dealer-list')}?highlight=dealer-{self.object.id}"
