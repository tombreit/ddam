from pathlib import Path
from collections import namedtuple
from PIL import Image

from django.conf import settings


def get_media_path(givenpath):
    givenpath = Path(givenpath)
    return f"/{givenpath.relative_to(settings.MEDIA_ROOT.parent)}"


def get_or_create_rendition(image, filepath):
    Rendition = namedtuple(
        "Rendition",
        "url width height"
    )

    if Path(image).suffix.lower() == ".svg":
        # Currently we bypass/ignore SVG files and do not
        # generate a bitmap rendition for it.
        rendition = Rendition(
            get_media_path(image),
            width=None,
            height=None,
        )

    elif filepath.is_file():
        # A rendition already exists, using this one
        with Image.open(filepath) as img_in_buffer:
            (width, height) = img_in_buffer.size

            rendition = Rendition(
                get_media_path(filepath),
                width,
                height,
            )
    else:
        # No existing rendition found, generating a new one
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(image, 'rb') as img_in, open(filepath, 'wb') as img_out:

            # https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#create-jpeg-thumbnails
            try:
                with Image.open(img_in) as img_in_buffer:
                    img_in_buffer.thumbnail(settings.IMG_RENDITION_LIST_SIZE)
                    img_in_buffer.save(img_out, "WEBP")
                    (width, height) = img_in_buffer.size

                    rendition = Rendition(
                        get_media_path(img_out.name),
                        width,
                        height,
                    )
            except OSError:
                print("Cannot create thumbnail for", img_in)

    return rendition


def get_rendition(image):
    asset_path = Path(image.name)
    rendition_filename = f"{asset_path.name}.webp"
    rendition_path = settings.IMG_RENDITION_ROOT / rendition_filename
    # Our image renditions are in webp image format:
    rendition_path.with_suffix('.webp')

    rendition = get_or_create_rendition(image.path, rendition_path)

    return rendition
