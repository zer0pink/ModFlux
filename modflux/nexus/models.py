from datetime import datetime
from typing import TypedDict


class NexusUser(TypedDict):
    user_id: int
    key: str
    name: str
    email: str
    profile_url: str
    is_premium: bool
    is_supporter: bool


class ModFile(TypedDict):
    id: int
    name: str
    version: str
    category_id: int
    category_name: str
    is_primary: bool
    size: int
    file_name: str
    uploaded_timestamp: datetime
    mod_version: str


class NexusDownload(TypedDict):
    game: str
    mod_id: int
    file_id: int
    download_url: str
    archive_path: str
    filename: str

    """
    The base name of the mod file without extension
    """
    name: str

    version: str
    published: int
