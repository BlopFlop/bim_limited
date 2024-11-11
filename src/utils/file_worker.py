import base64
from pathlib import Path


class DataBase64:
    """Class for work with Base64 data."""

    BASE64 = ";base64"

    def __init__(self, data: str):
        """Init current class."""
        full_data = data.split(self.BASE64)

        self.base64_data = full_data[-1]
        self.ext = full_data[0].split("/")[-1]
        self.type_data = full_data[0].split("/")[0].split(":")[-1]

    def save_file(self, name_file: str, path: Path) -> Path:
        """Save decode file."""
        full_name_file = f"{name_file}.{self.ext}"
        save_path: Path = path / full_name_file

        with open(save_path, 'wb') as img_file:
            decoded_img_data = base64.b64decode((self.base64_data))
            img_file.write(decoded_img_data)

        return save_path


def delete_file(path: Path) -> None:
    """Check or delete file."""
    if path.is_file():
        path.unlink()
