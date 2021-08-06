from io import BytesIO
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

from PIL import Image
def make_thumbnail(image_original):
    """
    Create and save the thumbnail for the photo (simple resize with PIL).
    """
    #fh = storage.open(image_original.name, 'r')
    try:
        image = Image.open(image_original)
    except:
        return False

    image.thumbnail((306,265), Image.ANTIALIAS)
    #fh.close()

    # Path to save to, name, and extension
    thumb_name, thumb_extension = os.path.splitext(image_original.name)
    thumb_extension = thumb_extension.lower()

    thumb_filename = thumb_name + '_thumb' + thumb_extension

    if thumb_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif thumb_extension == '.gif':
        FTYPE = 'GIF'
    elif thumb_extension == '.png':
        FTYPE = 'PNG'
    else:
        return False    # Unrecognized file type

    # Save thumbnail to in-memory file as StringIO
    temp_thumb = BytesIO()
    image.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)

    # Load a ContentFile into the thumbnail field so it gets saved
    #self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)

    return thumb_filename, ContentFile(temp_thumb.read())
