from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import DataTable, Footer

from controllers.service_locator import ServiceLocator
from managers.database_manager import DatabaseManager
from managers.game_state_manager import GameStateManager


class Leaderboard(Screen):
    """
    Represents a leaderboard screen that displays player scores including
    player name, number of moves, time taken, and the date played. The data
    is retrieved from the database and displayed in a sorted table format.
    """
    
    BINDINGS = [Binding("n", "back", "Back")]

    def compose(self) -> ComposeResult:
        table: DataTable = DataTable()
        keys = table.add_columns("Player Name", "Moves", "Time", "Date")

        database_manager = ServiceLocator.get(DatabaseManager)
        scores: list[tuple[str, int, int, str]] = database_manager.get_top_scores()
        for score in scores:
            player_name: str = score[0]
            moves: int = score[1]
            time_seconds: int = score[2]
            date_player: str = score[3]

            minutes, seconds = divmod(time_seconds, 60)
            hours, minutes = divmod(minutes, 60)

            table.add_row(player_name, moves, f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}", date_player)

        table.sort(keys[1])
        yield table

        yield Footer()

    def action_back(self) -> None:
        from screens.mode_selection import ModeSelectionScreen
        self.screen.app.push_screen(ModeSelectionScreen())

