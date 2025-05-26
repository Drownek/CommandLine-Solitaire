from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import RenderableType
from rich.panel import Panel
from textual.widget import Widget

from controllers.service_locator import ServiceLocator

if TYPE_CHECKING:
    from widgets.tableau import Pile
    from controllers.card_interact_controller import CardInteractController
    from managers.theme_manager import ThemeManager


class CardHolder(Widget):
    """
    Represents a card holder widget within the game, which serves as a place for cards that
    interact dynamically with other game components, such as piles, foundations, and waste.

    The class supports activities like rendering itself visually, managing class state related to
    invisibility, and handling card movements between various components based on specific game rules.

    :ivar pile: The pile associated with this card holder.
    :ivar foundation_index: Index in the foundation if the card holder belongs to a foundation.
    """

    def __init__(
        self,
        invisible: bool = False,
        pile: Pile | None = None,
        foundation_index: int | None = None,
        card_interact_controller: CardInteractController = None,
        theme_manager: ThemeManager = None,
    ):
        from controllers.card_interact_controller import CardInteractController
        from managers.theme_manager import ThemeManager

        super().__init__()
        self.pile = pile
        self.foundation_index = foundation_index
        if invisible:
            self.add_class("invisible")
        self._card_interact_controller = card_interact_controller or ServiceLocator.get(CardInteractController)
        self._theme_manager = theme_manager or ServiceLocator.get(ThemeManager)

    def copy(self) -> CardHolder:
        return CardHolder(self.has_class("invisible"))

    def render(self) -> RenderableType:
        box = self._theme_manager.get_box()
        assert box is not None
        return Panel.fit(
            "    ",
            border_style="dim",
            style="dim",
            box=box,
        )

    def on_click(self) -> None:
        self._card_interact_controller.handle_card_holder_click(self)
