from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from ddam.core.model_mixins import AbstractSingletonBaseModel


def validate_logo_image_file_extension(value):
    valid_extensions = ["svg"]
    return FileExtensionValidator(allowed_extensions=valid_extensions)(value)


class Branding(AbstractSingletonBaseModel):
    organization_name_en = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="Organization Name (EN)",
        default=_("A Company that Makes Everything"),
        help_text=_("Company, institute, site name (english version)."),
    )
    organization_name_de = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="Organization Name (DE)",
        default=_("A Company that Makes Everything"),
        help_text=_("Company, institute, site name (german version)."),
    )
    organization_abbr = models.CharField(
        max_length=255,
        blank=False,
        verbose_name="Abbreviation",
        default="ACME",
        help_text=_("Company, institute, site abbreviation."),
    )
    organization_street = models.CharField(
        max_length=255,
        blank=True,
        help_text="Street and house number. Used in printouts etc."
    )
    organization_zip_code = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Organization ZIP Code",
        help_text="Used in printouts etc."
    )
    organization_city = models.CharField(
        max_length=255,
        blank=True,
        help_text="Used in printouts etc."
    )
    organization_url = models.URLField(
        blank=True,
        verbose_name="Organization URL",
        help_text="Used in printouts etc."
    )
    organization_logo = models.FileField(
        null=True,
        blank=True,
        upload_to='branding/',
        validators=[validate_logo_image_file_extension],
        verbose_name="Logo file",
        help_text=_('Logo file. SVG, transparent background'),
    )
    organization_figurative_mark = models.FileField(
        null=True,
        blank=True,
        upload_to='branding/',
        validators=[validate_logo_image_file_extension],
        verbose_name="Figurative Mark/Bildmarke",
        help_text='Bildmarke, quasi Logo ohne Wortmarke.',
    )
    organization_favicon = models.FileField(
        null=True,
        blank=True,
        upload_to='branding/',
        validators=[validate_logo_image_file_extension],
        verbose_name="Favicon file",
    )
    documentation_url = models.URLField(
        blank=True,
        default="",
        help_text="If you host the documentation on your own, provide the URL here."
    )

    def __str__(self):
        return f"Branding for {self.organization_name_en or 'n/a'}"

    class Meta:
        verbose_name = "Branding"
        verbose_name_plural = "Branding"
