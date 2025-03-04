import os
from pathlib import Path
import logging


logger = logging.getLogger("modflux")

# XDG Base Directory Specification
XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
XDG_DATA_HOME = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
XDG_CACHE_HOME = os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))

# Application directories
APP_NAME = "modflux"
CONFIG_DIR = Path(XDG_CONFIG_HOME) / APP_NAME
DATA_DIR = Path(XDG_DATA_HOME) / APP_NAME
CACHE_DIR = Path(XDG_CACHE_HOME) / APP_NAME

# Ensure directories exist
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# File paths

GAME = None

# Where the extract mods live
MANAGED_MOD_DIR = None

# Where the base game is
BASE_GAME_PATH = None

# Where the mod archives are downloaded to
DOWNLOAD_PATH = None

# For Overlay
OVERLAY_FS_WORK_PATH = None
OVERLAY_FS_OVERWRITE_PATH = None

# Nexus
NEXUS_MODS_API_KEY = None

DATABASE_FILE = CONFIG_DIR / "modflux.db"
CONFIG_FILE = CONFIG_DIR / "config.yml"


# TODO clean this janky shit up

def initialize(game):
    logging.info("Loading profile data")

    global MANAGED_MOD_DIR, BASE_GAME_PATH, DOWNLOAD_PATH, OVERLAY_FS_OVERWRITE_PATH, OVERLAY_FS_WORK_PATH, GAME

    MANAGED_MOD_DIR = game.mod_path
    BASE_GAME_PATH = game.game_path
    DOWNLOAD_PATH = game.download_path
    OVERLAY_FS_OVERWRITE_PATH = game.overwrite_path
    OVERLAY_FS_WORK_PATH = game.work_path
    GAME = game 
