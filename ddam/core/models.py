import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from django.db import models
from django.db.models import Count
from django.urls import reverse


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
        return self.name

    class Meta:
        verbose_name = _("Usage tag")
        verbose_name_plural = _("Usage tags")


class SingletonBaseModel(models.Model):

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
        return self.title


class Asset(AbstractTimestampedModel, AbstractUserTrackedModel, AbstractUuidModel, models.Model):
    title = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
    )
    file = models.FileField(
        blank=False,
        upload_to='assets/',
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
    copyright_statement = models.CharField(
        max_length=255,
        blank=True,
        help_text="Appropriate credit/Licence holder (if required by license)",
    )
    usage_restriction = models.ForeignKey(
        'core.usagerestriction',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    usage = models.ManyToManyField(
        Usage,
        blank=True,
        verbose_name="Usage tag",
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

    def get_absolute_url(self):
        return reverse('core:asset-detail', kwargs={'id': self.id})

    def __str__(self):
        return self.title