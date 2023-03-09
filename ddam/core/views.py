from django.db.models import Count, Q
from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from .models import Asset, Licence, Usage
from .filters import AssetFilter
from .forms import MultiFileFieldForm, AssetForm


def asset_filter_list(request):
    f = AssetFilter(request.GET, queryset=Asset.objects.all())
    return render(request, 'core/asset_filter_list.html', {'filter': f})


class MultiFileFieldFormView(FormView):
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
                    created_by=request.user.email,
                )
                assets_upload.append(asset)
            
            print(f"{assets_upload=}")
            Asset.objects.bulk_create(assets_upload)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AssetListView(ListView):
    model = Asset
    context_object_name = "assets"

    def get_queryset(self):
        filter_expr = Q()
        
        tag = self.request.GET.get('tag')
        if tag:
            filter_expr = Q(tags__slug=tag)

        qs = (
            Asset
            .objects
            .filter(filter_expr)
            .distinct()
        )
        return qs


class AssetDetailView(DetailView):
    model = Asset
    pk_url_kwarg = "id"
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context


class AssetCreate(CreateView):
    model = Asset
    pk_url_kwarg = "id"
    form_class = AssetForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user.email
        return super().form_valid(form)


class AssetUpdate(UpdateView):
    model = Asset
    pk_url_kwarg = "id"
    form_class = AssetForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user.email
        return super().form_valid(form)


class UsageListView(ListView):
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


class UsageDetailView(DetailView):
    model = Usage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Asset.objects.filter(usage=self.kwargs['pk']).count()
        return context


class UsageCreateView(CreateView):
    model = Usage
    fields = [
        "name",
        "media",
        "notes",
    ]


class UsageUpdateView(UpdateView):
    model = Usage
    fields = [
        "name",
        "media",
        "notes",
    ]


class LicenceListView(ListView):
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


class LicenceDetailView(DetailView):
    model = Licence

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = Asset.objects.filter(licence=self.kwargs['pk']).count()
        return context

class LicenceCreate(CreateView):
    model = Licence
    fields = '__all__'


class LicenceUpdate(UpdateView):
    model = Licence
    fields = '__all__'