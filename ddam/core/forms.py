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


class MultiFileFieldForm(forms.Form):
    """
    https://docs.djangoproject.com/en/4.1/topics/http/file-uploads/#uploading-multiple-files
    """
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )


class AssetFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'asset-filter-form'
        self.helper.form_method = 'get'
        self.fields['licence'].label = mark_safe('<i class="bi bi-signpost-split"></i> Licence')
        self.fields['usage'].label = mark_safe('<i class="bi bi-diagram-2-fill"></i> Usage')
        self.helper.layout = Layout(
            Div(
                Field('title', wrapper_class='form-group col-md-4 pe-4'),
                InlineCheckboxes('usage', wrapper_class='form-group col-md-4 px-4'),
                InlineRadios('licence', wrapper_class='form-group col-md-4 ps-4'),
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
        self.fields['licence'].label = mark_safe('<i class="bi bi-signpost-split"></i> Licence')
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
                InlineRadios('licence'),
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
            "licence",
            "usage",
        ]
        widgets = {
            'licence': forms.RadioSelect,
            'usage': forms.CheckboxSelectMultiple,
        }
