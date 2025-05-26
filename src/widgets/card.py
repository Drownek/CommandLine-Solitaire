from __future__ import annotations

from typing import TYPE_CHECKING

from rich.box import Box
from rich.panel import Panel
from textual.reactive import reactive
from textual.widget import Widget

from constants import RED_SUITS
from controllers.service_locator import ServiceLocator
from managers.theme_manager import ThemeManager

if TYPE_CHECKING:
    from widgets.tableau import Pile
    from controllers.card_interact_controller import CardInteractController


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

    def __init__(
        self,
        suit: str,
        value: str,
        hidden: bool = False,
        card_controller: CardInteractController = None,
        theme_manager: ThemeManager = None,
        **kwargs,
    ):
        from controllers.card_interact_controller import CardInteractController

        super().__init__(**kwargs)
        self.suit = suit
        self.value = value
        self.hidden = hidden
        self._card_controller = card_controller or ServiceLocator.get(CardInteractController)
        self._theme_manager = theme_manager or ServiceLocator.get(ThemeManager)

    def __str__(self) -> str:
        return f"{self.suit}{self.value}"

    def __repr__(self) -> str:
        return f"{self.suit}{self.value}"

    def copy(self) -> Card:
        return Card(self.suit, self.value, self.hidden)

    def render(self) -> Panel:
        """Render the card as a Panel with appropriate styling based on card state."""
        self._set_card_color()
        content = self._generate_card_content()
        border_box = self._get_border_box()

        return Panel.fit(
            content,
            border_style=self.color,
            box=border_box,
            padding=(0, 0),
            title_align="left",
        )

    def _set_card_color(self) -> None:
        """Determine and set the appropriate color for the card based on suit and state."""
        is_red_suit = self.suit in RED_SUITS

        if self.hidden:
            self.color = "dim"
        elif self._theme_manager.current_theme != "rainbow":
            self.color = "red" if is_red_suit else "white"

    def _generate_card_content(self) -> str:
        """Generate the visible content for the card based on its state."""
        display_value = "?" if self.hidden else self.value
        display_symbol = "?" if self.hidden else self.suit
        # More space needed for single-digit cards to align properly
        spacing = "   " if len(display_value) == 2 else "    "

        return f"[{self.color}]{display_symbol}{display_value}[/][{self.color}][/]{spacing}\n\n\n"

    def _get_border_box(self) -> Box:
        """Get the appropriate border box based on the card's selection state."""
        border_box = (
            self._theme_manager.get_selected_box()
            if self.is_selected()
            else self._theme_manager.get_box()
        )
        assert border_box is not None
        return border_box

    def on_click(self) -> None:
        self._card_controller.handle_card_click(self)

    def hide(self) -> None:
        self.hidden = True
        self.refresh()

    def unhide(self) -> None:
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
