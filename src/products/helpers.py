import os
import re
import uuid


def product_image_path(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("product_thumbnails/", new_filename)


def generate_product_id(name: str) -> str:
    name = re.sub(" +", " ", name)
    return name.strip().lower().replace(" ", "-")


def format_barcode(device_id: int):
    return f"device_{device_id:09d}"


def decode_device_id(barcode: str) -> int:
    try:
        return int(barcode.replace("device_", ""))
    except ValueError:
        return 0
