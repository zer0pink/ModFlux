import os
import pathlib
import zipfile

import rarfile
import py7zr
from urllib.parse import parse_qs, unquote, urlparse
import re
from pathlib import Path
from typing import Tuple

from modflux import nexus
from modflux.nexus import NexusDownload
from modflux import config


def extract_mod_archive(filename: str) -> str:
    """
    Extracts a zip or rar file to a new directory within the managed mods directory.

    Args:
        filename: Path to the archive file (zip or rar)
        managed_mods_dir: Base directory where mods should be extracted

    Returns:
        str: The full archive name without the extension

    Raises:
        zipfile.BadZipFile: If the zip file is invalid
        rarfile.BadRarFile: If the rar file is invalid
        OSError: If there are file system related errors
        ValueError: If the file type is not supported
    """
    file_path = Path(filename)
    file_extension = file_path.suffix.lower()

    # Get the archive name without extension to use as directory name
    archive_name = file_path.stem

    # Create the full path for the extraction directory
    extract_dir = os.path.join(config.MANAGED_MOD_DIR, archive_name)

    # Create the directory if it doesn't exist
    os.makedirs(extract_dir, exist_ok=True)

    # Extract based on file type
    if file_extension == ".zip":
        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
    elif file_extension == ".rar":
        with rarfile.RarFile(filename, "r") as rar_ref:
            rar_ref.extractall(extract_dir)
    elif file_extension == ".7z":
        with py7zr.SevenZipFile(filename, mode="r") as archive:
            archive.extractall(extract_dir)
    else:
        raise ValueError(f"Unsupported archive format: {file_extension}")

    return archive_name


def nxm_process(nxm: str) -> NexusDownload:
    """
    Process a NXM link and get a bunch of details about it

    Args:
        nxm: str: A nxm:// URL to download
    """

    # break down the URL
    parsedUrl = urlparse(nxm)
    query = parse_qs(parsedUrl.query)

    # Need to breakup the path
    paths = parsedUrl.path.split("/")

    # Get the important bits
    game = parsedUrl.netloc
    mod_id = paths[2]
    file_id = paths[4]

    # [{'name': 'Nexus Global Content Delivery Network', 'short_name': 'Nexus CDN', 'URI': 'https://supporter-files.nexus-cdn.com/3333/4198/ArchiveXL-4198-1-21-1-1737797101.zip?md5=GpfQ5USDsSRDPcOoCD_NYA&expires=1739817809&user_id=122332413'}]
    result = nexus.getClient().get_mod_file_download_link(
        game_domain_name=game,
        mod_id=mod_id,
        file_id=file_id,
        key=query["key"][0],
        expires=query["expires"][0],
    )

    # TODO Look at the API responses here and determine what else can come in
    url = result[0]["URI"]

    # Extract filename from URL
    # First try to get it from the path
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # Remove any query parameters from filename if present
    filename = filename.split("?")[0]

    # URL decode the filename
    filename = unquote(filename)

    # Construct the full save path
    archive_path = os.path.join(config.DOWNLOAD_PATH, filename)

    file_info = nexus.getClient().get_mod_file(
        game_domain_name=game, mod_id=mod_id, file_id=file_id
    )

    return {
        "game": game,
        "mod_id": mod_id,
        "file_id": file_id,
        "download_url": url,
        "filename": filename,
        "name": pathlib.Path(filename).stem,
        "archive_path": archive_path,
        "version": file_info["version"],
        "published": file_info["uploaded_timestamp"],
    }


def parse_filename(filename: str) -> Tuple[str, str, str, str]:
    """
    Parse filenames to extract mod name and version number into a dictionary.

    Args:
        filename (str): List of filename strings to parse

    Returns:
        dict: Dictionary with mod names as keys and version numbers as values
    """
    pattern = r"^(.+?)-(\d+)-(.+?)-(\d+)\."
    match = re.match(pattern, filename)
    print(match)
    if match:
        name = match.group(1)
        id = match.group(2)
        version = match.group(3)
        published = match.group(4)

    return (name, id, version, published)
