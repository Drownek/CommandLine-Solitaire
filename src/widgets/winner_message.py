from __future__ import annotations

from pygame.mixer import Sound
from textual import on
from textual.app import ComposeResult
from textual.containers import Center
from textual.reactive import reactive
from textual.validation import Length
from textual.widget import Widget
from textual.widgets import Static, Input, Button

from controllers.service_locator import ServiceLocator
from managers.database_manager import DatabaseManager
from screens.leaderboard import Leaderboard
from widgets.time_display import TimeDisplay


class WinnerMessage(Widget):
    """
    Represents the winner message displayed after completing the game.

    This class is responsible for presenting the winning message, collecting the player's
    name, and saving the player's score to the database. It also handles playing the
    winning sound and interacting with the game state and database managers.
    """

    moves = reactive(0, recompose=True)

    def compose(self) -> ComposeResult:
        yield Static(f"🎉 W I N N E R ! 🎉\n\nYou solved pasjans in {self.moves} move{self._plural(self.moves)}.\n\n",
                     id="winner-text")
        yield Input(placeholder="Player name", id="winner-name", validators=Length(4, 16))
        with Center():
            yield Button("Save score", id="save-score")

    @on(Button.Pressed)
    def save_score(self) -> None:
        from pasjans import GameHeader

        winner_name_input = self.screen.query_one("#winner-name", Input)
        if not winner_name_input.is_valid:
            self.notify("Podaj nazwę od 4 do 16 znaków!")
            return
        winner_name = winner_name_input.value
        time_display: TimeDisplay = self.screen.query_one(TimeDisplay)
        game_header: GameHeader = self.screen.query_one(GameHeader)
        moves = game_header.moves
        database_manager = ServiceLocator.get(DatabaseManager)
        database_manager.save_score(winner_name, moves, time_display.time)
        self.screen.app.push_screen(Leaderboard())

    @staticmethod
    def _plural(value: int) -> str:
        return "" if value == 1 else "s"

    def show(self, moves: int) -> None:
        Sound("./sounds/winscreen.ogg").play()
        self.moves = moves
        self.add_class("visible")
        time_display: TimeDisplay = self.screen.query_one(TimeDisplay)
        time_display.stop()

    def hide(self) -> None:
        self.remove_class("visible")
