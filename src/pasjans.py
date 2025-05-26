from __future__ import annotations

import pygame
from textual.app import App

from controllers.service_locator import ServiceLocator
from managers.database_manager import DatabaseManager
from managers.game_state_manager import GameStateManager
from managers.move_event_manager import MoveEventManager
from managers.theme_manager import ThemeManager
from screens.help import Help
from screens.mode_selection import ModeSelectionScreen


class Pasjans(App[None]):
    """
    A class representing a Pasjans application.

    Pasjans is a card game application with a structured layout and settings.
    It is developed as part of a specific framework extending the App class.
    This class defines basic configurations, available screens, and the main
    entry point for mounting custom screens.

    :ivar ENABLE_COMMAND_PALETTE: Indicates whether the command palette feature
        is enabled. Default is False.
    :ivar CSS_PATH: Path to the styling file for the application's user
        interface.
    :ivar SCREENS: A dictionary mapping screen identifiers to their
        corresponding screen classes.
    :ivar TITLE: Title of the application displayed in the UI.
    """

    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = "pasjans.tcss"
    SCREENS = {"help": Help}
    TITLE = "Pasjans Gigathon"

    def __init__(self) -> None:
        super().__init__()
        ServiceLocator.register(DatabaseManager, DatabaseManager())
        ServiceLocator.register(GameStateManager, GameStateManager())
        ServiceLocator.register(MoveEventManager, MoveEventManager())
        ServiceLocator.register(ThemeManager, ThemeManager())

    def on_mount(self) -> None:
        pygame.mixer.init()
        self.push_screen(ModeSelectionScreen())
