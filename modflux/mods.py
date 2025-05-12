import logging
import os
from typing import List

import sh
from peewee import fn

from modflux import utils
from modflux.db import Game, Mod, ModVersion
from modflux.nexus.models import NexusDownload
from modflux.game_manager import GameManager

logger = logging.getLogger("modflux")

fuse = sh.Command("fuse-overlayfs")

HARDLINK_MODE = False
HARDLINK_STAGING_DIR = "/mnt/games2/cyberpunk/staging"


def process_download(nexus_download: NexusDownload):
    """Process a completed download"""
    mod_path = utils.extract_mod_archive(nexus_download["archive_path"])

    version = ModVersion.create(
        nexus_mod_id=nexus_download["mod_id"],
        nexus_file_id=nexus_download["file_id"],
        version=nexus_download["version"],
        path=mod_path,
        game_id=_game().id,
    )

    load_order = get_next_load_order()

    mod = Mod.create(
        name=nexus_download["name"],
        load_order=load_order,
        nexus_mod_id=nexus_download["mod_id"],
        version=version,
        active=True,
        game_id=_game().id,
    )

    return mod


def import_mod(file_name: str) -> Mod:
    # Extract the mod
    archive_name = os.path.basename(file_name)
    mod_name = utils.extract_mod_archive(file_name)

    # Get next load order
    load_order = get_next_load_order()

    name, mod_id, version, _ = utils.parse_filename(archive_name)

    # Create version entry
    version = ModVersion.create(
        version=version,  # Version from filename
        path=mod_name,
        nexus_mod_id=mod_id,
        game_id=_game().id,
    )

    # Create mod entry
    mod = Mod.create(
        name=name,
        load_order=load_order,
        version=version,
        active=True,
        nexus_mod_id=mod_id,
        game_id=_game().id,
    )

    return mod


def link():
    target_dir = HARDLINK_STAGING_DIR

    mods = (
        Mod.select()
        .join(ModVersion)
        .order_by(Mod.load_order.desc())
        .where(Mod.active, Mod.game_id == _game().id)
    )

    for mod in mods:
        source_dir = str(os.path.join(_game().mod_path, mod.version.path))

        # Walk through the source directory recursively
        for root, dirs, files in os.walk(source_dir):
            # Calculate the relative path from source_dir
            rel_path = os.path.relpath(root, source_dir)

            # Create the corresponding directory in the target
            target_path = os.path.join(target_dir, rel_path)
            if rel_path != ".":  # Skip for the root directory
                os.makedirs(target_path, exist_ok=True)

            # Process each file
            for file in files:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_path, file)

                try:
                    # Create directories if they don't exist
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)

                    # Create a hard link
                    if os.path.exists(target_file):
                        print(
                            f"Warning: Target file already exists: '{target_file}'. Skipping."
                        )
                        # error_count += 1
                    else:
                        os.link(source_file, target_file)
                        # file_count += 1
                        print(f"Created hardlink: {target_file}")

                except Exception as e:
                    print(f"Error creating hardlink for '{source_file}': {e}")
                    # error_count += 1


def mount_with_fuse(mounts: list) -> bool:
    """Helper function to handle fuse mounting with given mounts"""
    mod_mounts = ":".join(mounts)

    try:
        fuse(
            "-o",
            f"workdir={_game().work_path},upperdir={_game().overwrite_path},lowerdir={mod_mounts}",
            _game().game_path,
            _cwd=_game().mod_path,
        )
        return True
    except Exception as e:
        logger.error(e)
        return False


def mount() -> bool:
    """Mount the mod overlay filesystem"""
    mounts = []

    if not HARDLINK_MODE:
        # Get mods ordered by load order
        mods = (
            Mod.select()
            .join(ModVersion)
            .order_by(Mod.load_order.desc())
            .where(Mod.active, Mod.game_id == _game().id)
        )

        # Build mounts list from mod versions
        for mod in mods:
            mounts.append(mod.version.path)

    else:
        logger.debug("Mounting in hardlink mode")
        mounts.append(HARDLINK_STAGING_DIR)

    # Add base game path to mounts
    mounts.append(_game().game_path)

    return mount_with_fuse(mounts)


def unmount() -> bool:
    try:
        sh.fusermount3("-u", _game().game_path)
    except Exception as e:
        logger.error(e)
        return False

    return True


def is_active() -> bool:
    try:
        # Exit code 0 means the dir is a mountpoint
        sh.mountpoint(_game().game_path)
        return True
    except sh.ErrorReturnCode_32:
        # Is not a mount point
        return False
    except sh.ErrorReturnCode as e:
        # Unknown
        raise e


def get_game_mods() -> List[Mod]:
    return list(
        Mod.select()
        .join(ModVersion)
        .join(Game)
        .where(Game.id == _game().id)
        .order_by(Mod.load_order)
    )


def get_next_load_order() -> int:
    load_order = (
        Mod.select(fn.MAX(Mod.load_order)).where(Mod.game_id == _game().id).scalar()
    )
    if load_order is None:
        return 0
    else:
        return load_order + 1


def mod_latest(game: str, mod: Mod) -> str:
    """
    Return the latest
    """
    pass
    # mod_info = nmm.get_mod_info(game_domain_name=game, mod_id=mod.nexus_mod_id)
    # mod.latest_version = mod_info["version"]
    # mod.save()

    # return mod_info["version"]


def update_mods_latest_version():
    mods = Mod.select(fn.Distinct(Mod.id)).execute()

    for mod in mods:
        mod_latest(_game().id, mod.mod_id)


def _game() -> Game:
    return GameManager.get_instance().game
