from django import forms
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, HTML, Div, Field
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import (
    InlineCheckboxes,
    InlineRadios,
)

from .models import Asset


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultiFileFieldForm(forms.Form):
    """
    https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/#uploading-multiple-files
    """
    file_field = MultipleFileField()


class AssetFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'asset-filter-form'
        self.helper.form_method = 'get'
        self.fields['license'].label = mark_safe('<i class="bi bi-signpost-split"></i> License')
        self.fields['usage'].label = mark_safe('<i class="bi bi-diagram-2-fill"></i> Usage')
        self.helper.layout = Layout(
            Div(
                Field('title', wrapper_class='form-group col-md-4 pe-4'),
                InlineCheckboxes('usage', wrapper_class='form-group col-md-4 px-4'),
                InlineRadios('license', wrapper_class='form-group col-md-4 ps-4'),
                css_class="row"
            ),
            HTML("""
            <button class="btn btn-primary"><i class="bi bi-search-heart-fill"></i> Search</button>
            """),
            HTML("""
                <a class="btn btn-secondary" href=".">Reset</a>
            """),
        )


class AssetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'asset-form'
        self.helper.form_method = 'post'
        self.fields['with_costs'].label = mark_safe('<i class="bi bi-coin"></i> Paid for?')
        self.fields['license'].label = mark_safe('<i class="bi bi-signpost-split"></i> License')
        self.fields['usage'].label = mark_safe('<i class="bi bi-diagram-2-fill"></i> Usage')
        self.helper.layout = Layout(
            FloatingField('title'),
            Field('file'),
            FloatingField('description'),
            Fieldset("Aquisition",
                FloatingField('source_url'),
                Div(
                    Div(
                        FloatingField('dealer'),
                        css_class="flex-fill me-4",
                    ),
                    Div(
                        Field('with_costs', css_class="form-check-input", wrapper_class="form-check form-switch"),
                        css_class="flex-fill",
                    ),
                    css_class="d-flex mb-2",
                ),
                FloatingField('copyright_statement'),
                InlineRadios('license'),
                css_class="bg-light rounded p-4 my-4",
            ),
            Div(
                InlineCheckboxes('usage'),
                css_class="me-4 p-4 bg-light rounded"
            ),
            HTML("""
            <button type="submit" class="btn btn-primary">
                Submit
            </button>
            """),
            HTML("""
                <a class="btn btn-secondary" href=".">Reset</a>
            """),
        )

    class Meta:
        model = Asset
        fields = [
            "title",
            "file",
            "description",
            "copyright_statement",
            "source_url",
            "dealer",
            "with_costs",
            "license",
            "usage",
        ]
        widgets = {
            'license': forms.RadioSelect,
            'usage': forms.CheckboxSelectMultiple,
        }
