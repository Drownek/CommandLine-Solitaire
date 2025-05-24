from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Markdown, Footer


class Help(Screen):
    """
    Represents a help screen in the application.

    This class is used to display instructions, controls, and rules for the game.
    It provides a user-friendly guidance interface for players, including a detailed
    description of gameplay and controls.

    :ivar BINDINGS: A predefined list of key bindings for closing the help screen.
    """

    BINDINGS = [("escape,space,q,question_mark", "app.pop_screen", "Close")]

    def compose(self) -> ComposeResult:
        markdown_content = """
# Pasjans Gigathon
## Play instructions
### Rules of the game
The goal of the game is to arrange all the cards in the final four stacks by color and value (from ace to king). The cards can be stacked in the columns of the board in descending order and alternating colors.
### Keys
- **n** - New game
- **u** - Undo
- **?** - Help
- **q** - Exit
### Controls
- Click on a hidden card from the stack to reveal cards
- Click a card from the top to select it. 
- Click a card from under the top to select all cards from the top card to the current card
- When one card is selected, if rules allow, you can move it:
  - to the end stack by clicking on it
  - to another card from another stack by clicking on the top card
- When multiple cards are marked, you can only move them to another column by clicking on the top card

*Good luck!*
        """
        yield Markdown(markdown_content)
        yield Footer()
