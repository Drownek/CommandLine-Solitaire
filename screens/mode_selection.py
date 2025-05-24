from __future__ import annotations

from pathlib import Path

import pygame.mixer
from pygame.mixer import Sound
from textual import on
from textual.app import ComposeResult
from textual.containers import Middle, Center
from textual.screen import Screen
from textual.widgets import Label, Button

from managers.database_manager import DatabaseManager
from managers.game_state_manager import GameStateManager
from screens.leaderboard import Leaderboard


class ModeSelectionScreen(Screen):
    """
    This class provides a user interface to choose the difficulty level of the game.
    It displays two buttons, "Easy" and "Hard," and handles user input accordingly.
    When either button is pressed, it navigates to the game screen with the selected
    difficulty.
    """

    def __init__(self, database_manager: DatabaseManager, game_state_manager: GameStateManager):
        super().__init__()
        self.game_state_manager = game_state_manager
        self.database_manager = database_manager
        
        base_path = Path(__file__).resolve().parent.parent
        sound_path = base_path / "sounds" / "lobby.mp3"
        Sound(str(sound_path)).play(-1)

    def compose(self) -> ComposeResult:
        with Middle():
            with Center():
                yield Label(
                    """
        ██████╗  █████╗ ███████╗     ██╗ █████╗ ███╗   ██╗███████╗
        ██╔══██╗██╔══██╗██╔════╝     ██║██╔══██╗████╗  ██║██╔════╝
        ██████╔╝███████║███████╗     ██║███████║██╔██╗ ██║███████╗
        ██╔═══╝ ██╔══██║╚════██║██   ██║██╔══██║██║╚██╗██║╚════██║
        ██║     ██║  ██║███████║╚█████╔╝██║  ██║██║ ╚████║███████║
        ╚═╝     ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
                    """
                )
            with Center():
                yield Label("Select Difficulty Level:", id="choose-mode-label")
            with Center(id="button-group"):
                yield Button("Easy", id="easy")
                yield Button("Hard", id="hard")
            with Center():
                yield Button("Show Leaderboard", id="leaderboard")

    @on(Button.Pressed)
    def button_pressed(self, event: Button.Pressed) -> None:
        from pasjans import Game
        pygame.mixer.stop()
        match event.button.id:
            case "easy":
                self.screen.app.push_screen(Game(True, self.game_state_manager))
            case "hard":
                self.screen.app.push_screen(Game(False, self.game_state_manager))
            case "leaderboard":
                self.screen.app.push_screen(Leaderboard(self.database_manager, self.game_state_manager))
