import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images"
IMAGES_URL = "/images"

ALLOWED_TYPES = {
    "image/jpeg": "jpeg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/bmp": "bmp",
    "image/webp": "webp",
    "image/heic": "heic",
}

ALLOWED_FOLDERS = {
    "users"
}

IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def save_image(file: UploadFile, folder: str) -> str:
    if folder not in ALLOWED_FOLDERS:
        raise HTTPException(
            status_code=400,
            detail="Folder or model not allowed"
        )

    extension = ALLOWED_TYPES.get(file.content_type)

    if not extension:
        raise HTTPException(
            status_code=415,
            detail="Image format not supported"
        )

    content = file.file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The image file is empty"
        )

    folder_path = IMAGES_DIR / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    file_name = f"{folder}_{uuid.uuid4().hex}.{extension}"

    (folder_path / file_name).write_bytes(content)

    return f"{IMAGES_URL}/{folder}/{file_name}"