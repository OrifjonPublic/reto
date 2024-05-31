from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Your imports...

def decrease(images):
    l = []
    for value in images:
        if value:
                img = Image.open(value)
                img_format = img.format
                output = BytesIO()
                
                # For JPEG images
                if img_format in ['JPEG', 'jpeg', 'JPG', 'jpg', 'Jpeg']:
                    # Reduce the image size by adjusting the quality.
                    # This will reduce the volume while maintaining an acceptable quality.
                    img.save(output, format=img_format, quality=85, optimize=True)
                
                # For PNG images, we can use the optimization feature without affecting quality.
                elif img_format in ['PNG', 'png', 'Png']:
                    img.save(output, format=img_format, optimize=True)

                # Adjust output file for InMemoryUploadedFile
                new_image = InMemoryUploadedFile(
                    output, 'ImageField', f"{value.name}", f'image/{img_format.lower()}', 
                    sys.getsizeof(output), None
                )
                img.close()
                l.append(new_image)
    return l