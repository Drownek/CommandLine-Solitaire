from __future__ import annotations

from pygame.mixer import Sound
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer

from controllers.card_interact_controller import CardInteractController
from controllers.service_locator import ServiceLocator
from managers.game_state_manager import GameStateManager
from managers.theme_manager import ThemeManager
from widgets.game_header import GameHeader
from widgets.game_layout import GameLayout
from widgets.winner_message import WinnerMessage


class Game(Screen):
    """
    Represents the Game class, which extends the Screen class, and defines the main logic and
    user interaction for the game.

    This class contains methods for managing the game state, handling user actions, and
    rendering UI components such as the game header, grid, footer, and winner message. Game
    also includes static methods to handle pre-move and post-move events for tracking moves
    and determining the game's completion.
    """

    def __init__(self, easy_mode: bool, infinite_undo: bool, game_state_manager: GameStateManager = None, theme_manager: ThemeManager = None):
        super().__init__()
        ServiceLocator.register(CardInteractController, CardInteractController(self.screen, easy_mode))
        self.easy_mode = easy_mode
        self.infinite_undo = infinite_undo
        self._game_state_manager = game_state_manager or ServiceLocator.get(GameStateManager)
        self._theme_manager = theme_manager or ServiceLocator.get(ThemeManager)

    BINDINGS = [
        Binding("n", "new_game", "New Game"),
        Binding("u", "undo", "Undo"),
        Binding("question_mark", "app.push_screen('help')", "Help", key_display="?"),
        Binding("q", "app.quit", "Quit"),
        Binding("c", "change_theme", "Change Theme"),
    ]

    def compose(self) -> ComposeResult:
        yield GameHeader(self.infinite_undo)
        yield GameLayout()
        yield Footer()
        yield WinnerMessage()
        Sound("sounds/shuffle.ogg").play()

    def action_undo(self) -> None:
        self._game_state_manager.undo_last_operation(self.screen)

    def action_new_game(self) -> None:
        self.screen.app.pop_screen()

    def action_change_theme(self) -> None:
        self._theme_manager.switch_theme(self.screen)
        self.notify(f"Changed theme to '{self._theme_manager.current_theme}'")
