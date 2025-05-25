from __future__ import annotations

from typing import TYPE_CHECKING

from rich.panel import Panel
from textual.widget import Widget

from controllers.card_interact_controller import CardInteractController
from controllers.service_locator import ServiceLocator

if TYPE_CHECKING:
    from widgets.tableau import Pile


class CardHolder(Widget):
    """
    Represents a card holder widget within the game, which serves as a place for cards that
    interact dynamically with other game components, such as piles, foundations, and waste.

    The class supports activities like rendering itself visually, managing class state related to
    invisibility, and handling card movements between various components based on specific game rules.

    :ivar pile: The pile associated with this card holder.
    :ivar foundation_index: Index in the foundation if the card holder belongs to a foundation.
    """

    def __init__(self, invisible: bool = False, pile: Pile | None = None, foundation_index: int | None = None):
        super().__init__()
        self.pile = pile
        self.foundation_index = foundation_index
        if invisible:
            self.add_class("invisible")

    def copy(self) -> CardHolder:
        return CardHolder(self.has_class("invisible"))

    def render(self):
        from managers.theme_manager import ThemeManager
        box = ThemeManager.get_box()
        assert box is not None
        return Panel.fit(
            "    ",
            border_style="dim",
            style="dim",
            box=box,
        )

    def on_click(self) -> None:
        controller = ServiceLocator.get(CardInteractController)
        controller.handle_card_holder_click(self)