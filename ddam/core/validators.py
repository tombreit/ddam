import os
import mimetypes

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _

import magic


def _get_mimetypes_for_extensions(file_extensions: list) -> list:
    """
    Todo: also check for common, but not standardized mime types:
    https://docs.python.org/3.7/library/mimetypes.html#mimetypes.common_types
    """
    valid_mimetypes = []
    for ext in file_extensions:
        if not ext.startswith('.'):
            ext = "." + ext

        if mimetypes.types_map.get(ext):
            valid_mimetypes.append(mimetypes.types_map.get(ext))

    return valid_mimetypes


def validate_fileextension(value):
    """
    Validate if file extension is in list of allowed file extensions.
    """
    DDAM_ASSET_VALID_FILE_EXTENSIONS = settings.DDAM_ASSET_VALID_FILE_EXTENSIONS
    return FileExtensionValidator(allowed_extensions=DDAM_ASSET_VALID_FILE_EXTENSIONS)(value)


def validate_filetype(value):
    """
    Validate if mime type of uploaded file is in list of allowed mime types.
    """
    valid_mime_types = _get_mimetypes_for_extensions(settings.DDAM_ASSET_VALID_FILE_EXTENSIONS)
    file_mime_type = magic.from_buffer(value.read(2048), mime=True)

    if file_mime_type not in valid_mime_types:
        _msg = f'Unsupported file type. Valid mime types: `{", ".join(valid_mime_types)}`, got `{file_mime_type}`!'
        raise ValidationError(_msg)


def validate_filesize(value):
    """
    Validate if filesize is below max allowed file size.
    """
    max_file_size = settings.DDAM_ASSET_MAX_FILESIZE
    if value.size > max_file_size:
        message = _(f'Please keep file size under {filesizeformat(max_file_size)}. Current size is {filesizeformat(value.size)}.')
        code = "max_filesize_exceeded"
        raise forms.ValidationError(message, code=code)
