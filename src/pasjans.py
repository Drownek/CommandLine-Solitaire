from __future__ import annotations

import pygame
from pygame.mixer import Sound
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Label, Footer

from constants import MAX_UNDO
from controllers.card_interact_controller import CardInteractController
from controllers.service_locator import ServiceLocator
from managers.database_manager import DatabaseManager
from managers.game_state_manager import GameState, GameStateManager
from managers.theme_manager import ThemeManager
from screens.help import Help
from screens.mode_selection import ModeSelectionScreen
from widgets.card import Card
from widgets.foundation import Foundation
from widgets.game_layout import GameLayout
from widgets.stash_waste import StashWaste
from widgets.tableau import Tableau
from widgets.time_display import TimeDisplay
from widgets.winner_message import WinnerMessage


class GameHeader(Widget):
    """
    This class represents a widget that displays game information including the
    title, number of moves the player has made, and the remaining undo actions.
    It is designed to be reactive, ensuring updates to its fields are dynamically
    reflected in the widget. The widget contains labels for each piece of
    information, organized in a horizontal layout.

    :ivar remaining_undo: Tracks the number of undo actions left for the player.
    :ivar moves: Tracks the number of moves performed by the player.
    """

    def __init__(self, infinite_undo: bool):
        super().__init__()
        if infinite_undo:
            self.remaining_undo = 9999

    remaining_undo = reactive(MAX_UNDO, recompose=True)
    moves = reactive(0, recompose=True)

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(self.app.title, id="app-title")
            yield Label(f"Moves: {self.moves}", id="moves")
            yield Label(f"Remaining undo: {self.remaining_undo}", id="remaining-undo")
            yield TimeDisplay(id="time")


class Game(Screen):
    """
    Represents the Game class, which extends the Screen class, and defines the main logic and
    user interaction for the game.

    This class contains methods for managing the game state, handling user actions, and
    rendering UI components such as the game header, grid, footer, and winner message. Game
    also includes static methods to handle pre-move and post-move events for tracking moves
    and determining the game's completion.
    """

    def __init__(self, easy_mode: bool, infinite_undo: bool):
        super().__init__()
        ServiceLocator.register(CardInteractController, CardInteractController(self.screen, easy_mode))
        self.easy_mode = easy_mode
        self.infinite_undo = infinite_undo

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
        game_state_manager = ServiceLocator.get(GameStateManager)
        game_state_manager.undo_last_operation(self.screen)

    def action_new_game(self) -> None:
        self.screen.app.pop_screen()

    def action_change_theme(self) -> None:
        ThemeManager.switch_theme(self.screen)
        self.notify(f"Changed theme to '{ThemeManager.current_theme}'")

    @staticmethod
    def on_post_move_event(screen: Screen) -> None:
        """Used for checking if game is won, and move count tracker"""
        Sound("sounds/flip.ogg").play()
        game_header: GameHeader = screen.query_one(GameHeader)
        game_header.moves += 1

        king_card_in_foundation_count = 0
        foundation: Foundation = screen.query_one(Foundation)

        card: Card | None
        for card in foundation.cards:
            if card is not None and card.value == "K":
                king_card_in_foundation_count += 1

        if king_card_in_foundation_count == 4:
            winner_message: WinnerMessage = screen.query_one(WinnerMessage)
            winner_message.show(game_header.moves)

    @staticmethod
    def on_pre_move_event(screen: Screen) -> None:
        """Used for tracking moves for undo operation"""
        foundation: Foundation = screen.query_one(Foundation)
        tableau: Tableau = screen.query_one(Tableau)
        stash_waste: StashWaste = screen.query_one(StashWaste)
        state = GameState(
            screen,
            [pile.deep_copy() for pile in tableau.piles],
            stash_waste.deep_copy_stash(),
            stash_waste.deep_copy_waste(),
            foundation.copy_cards()
        )
        GameStateManager.previous_states.append(state)


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

    def __init__(self):
        super().__init__()
        ServiceLocator.register(DatabaseManager, DatabaseManager())
        ServiceLocator.register(GameStateManager, GameStateManager())

    def on_mount(self) -> None:
        pygame.mixer.init()
        self.push_screen(ModeSelectionScreen())
