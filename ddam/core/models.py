import uuid
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from .image_helpers import get_rendition
from .validators import validate_fileextension, validate_filetype, validate_filesize


class AbstractSingletonBaseModel(models.Model):

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        abstract = True


class AbstractUuidModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class AbstractTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractUserTrackedModel(models.Model):
    created_by = models.EmailField(blank=True)
    updated_by = models.EmailField(blank=True)

    class Meta:
        abstract = True


class Usage(models.Model):

    class MediaChoices(models.TextChoices):
        WEB = 'WEB'
        PRINT = 'PRT'

    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
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
    def get_icon(self):
        icon = ''
        if self.media == self.MediaChoices.WEB:
            icon = '<i class="bi bi-globe"></i>'
        elif self.media == self.MediaChoices.PRINT:
            icon = '<i class="bi bi-printer"></i>'

        return mark_safe(icon)

    def get_absolute_url(self):
        return reverse('core:usage-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Usage")
        verbose_name_plural = _("Usage")


class Licence(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        blank=False,
        unique=True,
    )
    url = models.URLField(
        blank=True,
        null=True,
        unique=True,
        verbose_name="URL",
        help_text="URL of official licence text.",
    )

    def get_absolute_url(self):
        return reverse('core:licence-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class UsageRestriction(models.Model):
    """
    Class to model the usage restrictions.
    """
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title}"


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
    licence = models.ForeignKey(
        'core.licence',
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
        help_text="Appropriate credit/Licence holder (if required by license)",
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
        usage_slugs = self.usage.all().values_list("slug", flat=True)

        all_usage_queryset = (
            Usage
            .objects
            .annotate(
                count=Count('asset'),
            )
            .order_by("-count")
        )

        usage_qs = all_usage_queryset.filter(slug__in=usage_slugs)
        return usage_qs

    @property
    def get_image_rendition(self):        
        return get_rendition(self.file)

    def get_absolute_url(self):
        return reverse('core:asset-detail', kwargs={'id': self.id})

    def __str__(self):
        return f"{self.title}"


class Dealer(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
        help_text="Name of dealer/distributor/vendor.",
    )

    def get_absolute_url(self):
        return reverse('core:dealer-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='dealer_name_unique_constraint',
            ),
        ]