from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive

from widgets.card_holder import CardHolder

if TYPE_CHECKING:
    from widgets.card import Card


class Foundation(HorizontalGroup):
    """
    Represents a foundation in a card game.

    The Foundation class organizes and manages a set of cards placed in a
    foundation, which is a critical component of many card games. It provides
    functionality to hold and manage up to four cards or placeholders, enabling
    gameplay mechanics such as card placement and retrieval. The class is built
    on top of a horizontal layout for card organization and rendering.

    :ivar cards: The list representing the cards in the foundation. A value of
        None in the list represents an empty place in the foundation.
    """

    cards: reactive[list[Card | None]] = reactive(
        [None, None, None, None], recompose=True
    )

    def __init__(self, cards: list[Card | None] | None = None):
        super().__init__()
        if cards is None:
            cards = [None, None, None, None]
        self.cards = cards

    def compose(self) -> ComposeResult:
        for i, card in enumerate(self.cards):
            if card is None:
                yield CardHolder(foundation_index=i)
            else:
                card.offset = (0, 0)  # type: ignore
                yield card

    def copy_cards(self) -> list[Card | None]:
        return [card.copy() if card else None for card in self.cards]
