from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label

from constants import MAX_UNDO
from widgets.time_display import TimeDisplay


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
