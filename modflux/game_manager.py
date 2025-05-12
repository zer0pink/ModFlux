class GameManager:
    """
    A singleton class that manages a single Game instance.
    Provides global access to the Game instance throughout the application.
    """

    _instance = None
    _game = None

    def __new__(cls, game=None):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, game=None):
        # Only set the game if it's not already set and a new game is provided
        if game is not None and self._game is None:
            self._game = game

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of GameManager.
        Creates a new instance if none exists.
        """
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance

    @property
    def game(self):
        """
        Get the current Game instance.

        Returns:
            Game: The current game instance.

        Raises:
            RuntimeError: If no game has been set.
        """
        if self._game is None:
            raise RuntimeError("No game has been set in GameManager")
        return self._game

    def set_game(self, game):
        """
        Set the game instance.

        Args:
            game (Game): The game instance to set.
        """
        self._game = game
