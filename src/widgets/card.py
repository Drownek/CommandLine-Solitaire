from __future__ import annotations

from typing import TYPE_CHECKING

from rich.panel import Panel
from textual.reactive import reactive
from textual.widget import Widget

from controllers.card_interact_controller import CardInteractController
from controllers.service_locator import ServiceLocator
from managers.theme_manager import ThemeManager

if TYPE_CHECKING:
    from widgets.tableau import Pile


class Card(Widget):
    """
    Represents a playing card widget with rendering and interaction capabilities.

    This class models a playing card that can be displayed on the screen, interacted with, and manipulated.
    It supports operations such as clicking, hiding, selecting, rendering to the screen, and determining its
    placement within a deck, pile, or foundation.

    :ivar suit: The suit of the card (e.g., ♥, ♦, ♠, ♣).
    :ivar value: The value of the card (e.g., "A", "2", ... "K").
    :ivar hidden: Indicates if the card is in a hidden state or visible.
    """

    color = reactive("dim", recompose=True)

    def __init__(self, suit: str, value: str, hidden: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.suit = suit
        self.value = value
        self.hidden = hidden

    def __str__(self):
        return f"{self.suit}{self.value}"

    def __repr__(self):
        return f"{self.suit}{self.value}"

    def copy(self) -> Card:
        return Card(self.suit, self.value, self.hidden)

    def render(self) -> Panel:
        red = self.suit in ('♥', '♦')
        if self.hidden:
            self.color = "dim"
        elif ThemeManager.current_theme != "rainbow":
            self.color = "red" if red else "white"

        value: str = self.value if not self.hidden else '?'
        symbol_display = self.suit if not self.hidden else '?'

        spaces = "   " if len(value) == 2 else "    "
        content = f"[{self.color}]{symbol_display}{value}[/][{self.color}][/]{spaces}\n\n\n"

        if self.is_selected():
            border_box = ThemeManager.get_selected_box()
        else:
            border_box = ThemeManager.get_box()

        assert border_box is not None

        return Panel.fit(
            content,
            border_style=self.color,
            box=border_box,
            padding=(0, 0),
            title_align="left"
        )

    def on_click(self) -> None:
        controller = ServiceLocator.get(CardInteractController)
        controller.handle_card_click(self)

    def hide(self):
        self.hidden = True
        self.refresh()

    def unhide(self):
        self.hidden = False
        self.refresh()

    def get_pile(self) -> Pile | None:
        from widgets.tableau import Pile
        for pile in self.screen.query(Pile):
            if self in pile.cards:
                return pile
        return None

    def make_selected(self) -> None:
        self.add_class("selected")
        self.refresh()

    def make_unselected(self) -> None:
        self.remove_class("selected")
        self.refresh()

    def is_selected(self) -> bool:
        return self.has_class("selected")
