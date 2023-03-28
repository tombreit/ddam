from django.conf import settings
from django.db import models
from django.db.models import Count
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
# from django.utils.text import slugify

from .image_helpers import get_rendition
from .validators import validate_fileextension, validate_filetype, validate_filesize


from .model_mixins import (
    AbstractRelatedObjectMixin,
    AbstractTimestampedModel,
    AbstractUserTrackedModel,
    AbstractUuidModel,
)



class Usage(AbstractRelatedObjectMixin, AbstractUuidModel, AbstractTimestampedModel, AbstractUserTrackedModel):

    class MediaChoices(models.TextChoices):
        WEB = 'WEB'
        PRINT = 'PRT'

    title = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
    )
    notes = models.TextField(
        blank=True,
        help_text=_('E.g. usage information, URLs'),
    )
    media = models.CharField(
        max_length=3,
        choices=MediaChoices.choices,
    )

    @property
    def get_media_icon(self):
        icon = ''
        if self.media == self.MediaChoices.WEB:
            icon = '<i class="bi bi-globe"></i>'
        elif self.media == self.MediaChoices.PRINT:
            icon = '<i class="bi bi-printer"></i>'

        return mark_safe(icon)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Usage")
        verbose_name_plural = _("Usage")


class License(AbstractRelatedObjectMixin, AbstractUuidModel, AbstractTimestampedModel, AbstractUserTrackedModel):
    title = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        unique=True,
    )
    url = models.URLField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="URL",
        help_text="URL of official license text.",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")


class Dealer(AbstractRelatedObjectMixin, AbstractUuidModel, AbstractTimestampedModel, AbstractUserTrackedModel):
    title = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
        help_text="Name of dealer/distributor/vendor.",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("Dealer")
        verbose_name_plural = _("Dealers")
        constraints = [
            models.UniqueConstraint(
                Lower('title'),
                name='dealer_title_unique_constraint',
            ),
        ]


# class UsageRestriction(models.Model):
#     """
#     Class to model the usage restrictions.
#     """
#     title = models.CharField(max_length=255, blank=False)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.title}"


class Asset(AbstractTimestampedModel, AbstractUserTrackedModel, AbstractUuidModel, models.Model):
    title = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
    )
    file = models.FileField(
        blank=False,
        upload_to=settings.DDAM_ASSET_UPLOAD_DIR,
        validators=[
            validate_fileextension,
            validate_filetype,
            validate_filesize,
        ],
    )
    filename_orig = models.CharField(
        max_length=255,
        blank=False,
        editable=False,
        help_text="Original filename. Set automatically while creating an asset."
    )
    description = models.TextField(
        blank=True
    )
    license = models.ForeignKey(
        'core.license',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    dealer = models.ForeignKey(
        'core.dealer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    with_costs = models.BooleanField(
        default=False,
        help_text="If you actually paid for this asset, set this info here.",
    )
    copyright_statement = models.CharField(
        max_length=255,
        blank=True,
        help_text="Appropriate credit/License holder (if required by license)",
    )
    source_url = models.URLField(
        blank=True,
        verbose_name="Source URL",
        help_text="Source/Origin of asset. Give an URL."
    )
    usage = models.ManyToManyField(
        Usage,
        blank=True,
        verbose_name="Usage",
        help_text="In which context this asset is in use."
    )

    @property
    def get_usage_with_count(self):
        usage_ids = self.usage.all().values_list("id", flat=True)

        all_usage_queryset = (
            Usage
            .objects
            .annotate(
                count=Count('asset'),
            )
            .order_by("-count")
        )

        usage_qs = all_usage_queryset.filter(id__in=usage_ids)
        return usage_qs

    @property
    def get_image_rendition(self):        
        return get_rendition(self.file)

    def get_absolute_url(self):
        return reverse('core:asset-detail', kwargs={'id': self.id})

    def __str__(self):
        return f"{self.title}"
