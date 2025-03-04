import os
from typing import List
import sh
import logging

from peewee import fn

from modflux.db import Game, Mod, ModVersion
from modflux import utils
from modflux import config
from modflux.nexus import NexusDownload

logger = logging.getLogger("modflux")

fuse = sh.Command("fuse-overlayfs")


def process_download(nexus_download: NexusDownload):
    """Process a completed download"""
    mod_path = utils.extract_mod_archive(nexus_download["archive_path"])

    version = ModVersion.create(
        nexus_mod_id=nexus_download["mod_id"],
        nexus_file_id=nexus_download["file_id"],
        version=nexus_download["version"],
        path=mod_path,
        game_id=config.GAME.id,
    )

    load_order = get_next_load_order()

    mod = Mod.create(
        name=nexus_download["name"],
        load_order=load_order,
        nexus_mod_id=nexus_download["mod_id"],
        version=version,
        active=True,
        game_id=config.GAME.id,
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
        game_id=config.GAME.id,
    )

    # Create mod entry
    mod = Mod.create(
        name=name,
        load_order=load_order,
        version=version,
        active=True,
        nexus_mod_id=mod_id,
        game_id=config.GAME.id,
    )

    return mod


def mount() -> bool:
    mods = (
        Mod.select()
        .join(ModVersion)
        .order_by(Mod.load_order.desc())
        .where(Mod.active == True, Mod.game_id == config.GAME.id)
    )

    mounts = []
    for mod in mods:
        mounts.append(mod.version.path)

    mounts.append(config.BASE_GAME_PATH)

    mod_mounts = ":".join(mounts)

    logger.debug(mod_mounts)

    try:
        fuse(
            "-o",
            f"workdir={config.OVERLAY_FS_WORK_PATH},upperdir={config.OVERLAY_FS_OVERWRITE_PATH},lowerdir={mod_mounts}",
            config.BASE_GAME_PATH,
            _cwd=config.MANAGED_MOD_DIR,
        )

        return True
    except Exception as e:
        logger.error(e)
        return False


def unmount() -> bool:
    try:
        sh.fusermount3("-u", config.BASE_GAME_PATH)
    except Exception as e:
        logger.error(e)
        return False

    return True


def is_active() -> bool:
    try:
        # Exit code 0 means the dir is a mountpoint
        sh.mountpoint(config.BASE_GAME_PATH)
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
        .where(Game.id == config.GAME.id)
        .order_by(Mod.load_order)
    )


def get_next_load_order() -> int:
    load_order = (
        Mod.select(fn.MAX(Mod.load_order)).where(Mod.game_id == config.GAME.id).scalar()
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
    mods = Mod.select(fn.Distinct(Mod.mod_id)).execute()

    for mod in mods:
        mod_latest(config.GAME.game_id, mod.mod_id)
