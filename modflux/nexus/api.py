from typing import Optional, List, Dict
from typing import Self

import requests

from modflux.db import Setting
from modflux.nexus.models import NexusUser, ModFile


class NexusModsAPI:
    BASE_URL = "https://api.nexusmods.com/v1"
    _instance = None

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"apikey": api_key, "User-Agent": "Python-Modflux/1.0"}

    @classmethod
    def get_instance(cls) -> Self:
        if cls._instance is None:
            setting = Setting.get(Setting.key == "nexus_api_key")
            if setting and setting.value:
                cls._instance = NexusModsAPI(api_key=setting.value)
            else:
                raise RuntimeError("Missing Nexus API Key")
        return cls._instance

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> Dict:
        """Make a request to the Nexus Mods API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            API response as dictionary
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.request(
            method, url, headers=self.headers, params=params, data=data
        )
        response.raise_for_status()
        return response.json()

    def validate_api_key(self) -> NexusUser:
        """Validate the API key and get user information."""
        data = self._make_request("GET", "/users/validate.json")
        return NexusUser(**data)

    def get_games(self, include_unapproved: bool = False) -> List[Dict]:
        """Get list of all games on Nexus Mods.

        Args:
            include_unapproved: Whether to include unapproved games

        Returns:
            List of games
        """
        params = {"include_unapproved": include_unapproved}
        return self._make_request("GET", "/games.json", params=params)

    def get_game_info(self, game_domain_name: str) -> Dict:
        """Get information about a specific game.

        Args:
            game_domain_name: Game domain name (e.g., 'skyrim')

        Returns:
            Game information
        """
        return self._make_request("GET", f"/games/{game_domain_name}.json")

    def get_mod_info(self, game_domain_name: str, mod_id: int) -> Dict:
        """Get information about a specific mod.

        Args:
            game_domain_name: Game domain name
            mod_id: Mod ID

        Returns:
            Mod information
        """
        return self._make_request(
            "GET", f"/games/{game_domain_name}/mods/{mod_id}.json"
        )

    def get_mod_files(
        self, game_domain_name: str, mod_id: int, category: Optional[str] = None
    ) -> List[ModFile]:
        """Get list of files for a specific mod.

        Args:
            game_domain_name: Game domain name
            mod_id: Mod ID
            category: Filter by category (main, update, optional, old_version, miscellaneous)

        Returns:
            List of mod files
        """
        params = {"category": category} if category else None
        data = self._make_request(
            "GET", f"/games/{game_domain_name}/mods/{mod_id}/files.json", params=params
        )
        return [ModFile(**file) for file in data["files"]]

    def get_mod_file(self, game_domain_name: str, mod_id: int, file_id: int) -> ModFile:
        """Get list of files for a specific mod.

        Args:
            game_domain_name: Game domain name
            mod_id: Mod ID
            file_id: Mod file id

        Returns:
            List of mod files
        """
        return self._make_request(
            "GET", f"/games/{game_domain_name}/mods/{mod_id}/files/{file_id}.json"
        )

    def get_mod_file_download_link(
        self,
        game_domain_name: str,
        mod_id: int,
        file_id: int,
        key: Optional[str] = None,
        expires: Optional[int] = None,
    ) -> Dict:
        """Get download link for a specific mod file.

        Args:
            game_domain_name: Game domain name
            mod_id: Mod ID
            file_id: File ID
            key: Key provided by Nexus Mods Website (required for non-premium users)
            expires: Expiry time for the key

        Returns:
            Download link information
        """
        params = {}
        if key:
            params["key"] = key
        if expires:
            params["expires"] = expires

        return self._make_request(
            "GET",
            f"/games/{game_domain_name}/mods/{mod_id}/files/{file_id}/download_link.json",
            params=params,
        )

    def get_trending_mods(self, game_domain_name: str) -> List[Dict]:
        """Get trending mods for a specific game.

        Args:
            game_domain_name: Game domain name

        Returns:
            List of trending mods
        """
        return self._make_request(
            "GET", f"/games/{game_domain_name}/mods/trending.json"
        )

    def get_latest_added_mods(self, game_domain_name: str) -> List[Dict]:
        """Get latest added mods for a specific game.

        Args:
            game_domain_name: Game domain name

        Returns:
            List of latest added mods
        """
        return self._make_request(
            "GET", f"/games/{game_domain_name}/mods/latest_added.json"
        )

    def get_latest_updated_mods(self, game_domain_name: str) -> List[Dict]:
        """Get latest updated mods for a specific game.

        Args:
            game_domain_name: Game domain name

        Returns:
            List of latest updated mods
        """
        return self._make_request(
            "GET", f"/games/{game_domain_name}/mods/latest_updated.json"
        )

    def get_user_tracked_mods(self) -> List[Dict]:
        """Get list of mods being tracked by the current user.

        Returns:
            List of tracked mods
        """
        return self._make_request("GET", "/user/tracked_mods.json")

    def track_mod(self, game_domain_name: str, mod_id: int) -> Dict:
        """Track a mod for the current user.

        Args:
            game_domain_name: Game domain name
            mod_id: Mod ID

        Returns:
            Response data
        """
        data = {"mod_id": mod_id}
        params = {"domain_name": game_domain_name}
        return self._make_request(
            "POST", "/user/tracked_mods.json", params=params, data=data
        )

    def untrack_mod(self, game_domain_name: str, mod_id: int) -> Dict:
        """Untrack a mod for the current user.

        Args:
            game_domain_name: Game domain name
            mod_id: Mod ID

        Returns:
            Response data
        """
        data = {"mod_id": mod_id}
        params = {"domain_name": game_domain_name}
        return self._make_request(
            "DELETE", "/user/tracked_mods.json", params=params, data=data
        )

    def endorse_mod(
        self, game_domain_name: str, mod_id: int, version: Optional[str] = None
    ) -> Dict:
        """Endorse a mod.

        Args:
            game_domain_name: Game domain name
            mod_id: Mod ID
            version: Mod version

        Returns:
            Response data
        """
        data = {"version": version} if version else None
        return self._make_request(
            "POST", f"/games/{game_domain_name}/mods/{mod_id}/endorse.json", data=data
        )

    def abstain_mod(
        self, game_domain_name: str, mod_id: int, version: Optional[str] = None
    ) -> Dict:
        """Abstain from endorsing a mod.

        Args:
            game_domain_name: Game domain name
            mod_id: Mod ID
            version: Mod version

        Returns:
            Response data
        """
        data = {"version": version} if version else None
        return self._make_request(
            "POST", f"/games/{game_domain_name}/mods/{mod_id}/abstain.json", data=data
        )
