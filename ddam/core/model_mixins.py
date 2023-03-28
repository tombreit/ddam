import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe


class AbstractRelatedObjectMixin(models.Model):

    @classmethod
    def get_app_label_and_model_name(cls):
        app_label, model_name = cls._meta.label_lower.split(".")
        return app_label, model_name

    @classmethod
    def get_icon(cls):
        model_name = cls._meta.model_name
        icon_css_classes = settings.DDAM_ICONS_MAP.get(model_name)
        return mark_safe(f'<i class="{icon_css_classes}"></i>')

    @classmethod
    def create_url(self):
        app_label, model_name = self.get_app_label_and_model_name()
        create_url = f"{app_label}:{model_name}-create"
        return reverse(create_url)
    
    @classmethod
    def model_name(cls):
        _app_label, model_name = cls.get_app_label_and_model_name()
        return model_name

    @classmethod
    def model_verbose_name(cls):
        return cls._meta.verbose_name

    @classmethod
    def model_verbose_name_plural(cls):
        return cls._meta.verbose_name_plural

    def update_url(self):
        app_label, model_name = self.get_app_label_and_model_name()
        update_url = f"{app_label}:{model_name}-update"
        return reverse(update_url, kwargs={'id': self.id})

    def get_absolute_url(self):
        app_label, model_name = self.get_app_label_and_model_name()
        absolute_url = f"{app_label}:{model_name}-list"
        highlight_query_param = f"highlight=object-{self.id}"
        return f"{reverse(absolute_url)}?{highlight_query_param}"

    class Meta:
        abstract = True


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
    created_by = models.EmailField(blank=True, editable=False)
    updated_by = models.EmailField(blank=True, editable=False)

    class Meta:
        abstract = True
