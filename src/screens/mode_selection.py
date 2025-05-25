from __future__ import annotations

import pygame.mixer
from pygame.mixer import Sound
from textual import on
from textual.app import ComposeResult
from textual.containers import Middle, Center
from textual.screen import Screen
from textual.widgets import Label, Button

from screens.leaderboard import Leaderboard


class ModeSelectionScreen(Screen):
    """
    This class provides a user interface to choose the difficulty level of the game.
    It displays two buttons, "Easy" and "Hard," and handles user input accordingly.
    When either button is pressed, it navigates to the game screen with the selected
    difficulty.
    """

    def __init__(self):
        super().__init__()
        Sound("./sounds/lobby.mp3").play(-1)

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
                self.screen.app.push_screen(Game(True))
            case "hard":
                self.screen.app.push_screen(Game(False))
            case "leaderboard":
                self.screen.app.push_screen(Leaderboard())
