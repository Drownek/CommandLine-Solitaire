from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Vertical
from textual.reactive import reactive
from textual.widget import Widget


from widgets.card_holder import CardHolder


class Tableau(HorizontalGroup):
    """
    Represents a tableau in a card game layout.

    The Tableau class extends the HorizontalGroup to manage a collection
    of piles displayed horizontally. It provides functionality to organize
    and render the piles in a structured manner.

    :ivar piles: A list of `Pile` objects that the tableau manages.
    """

    piles = reactive([], recompose=True)

    def __init__(self, piles: list[Pile]):
        super().__init__()
        self.piles = piles

    def compose(self) -> ComposeResult:
        for pile in self.piles:
            yield pile


class Pile(Vertical):
    """
    Represents a vertical stack of Card objects that can be dynamically composed and managed.

    This class is designed to organize and render a vertical collection of cards. The cards
    can be manipulated, deeply copied, and unselected using the available methods. The offset
    of each card is adjusted dynamically based on its position in the stack. The composition
    logic yields appropriate widgets based on the state of the card collection.

    :ivar cards: The list of Card objects managed by this Pile. Each card's offset is adjusted
        dynamically based on its position in the list.
    """

    cards = reactive([], recompose=True)  # type: ignore

    def __init__(self, cards=None, *children: Widget):
        super().__init__(*children)
        if cards is None:
            cards = []
        self.cards = cards

    def compose(self) -> ComposeResult:
        if not self.cards:
            yield CardHolder(True, self)
            return

        for i, card in enumerate(self.cards):
            card.styles.offset = (0, -4 * i)
            yield card

    def deep_copy(self) -> Pile:
        copied_cards = [card.copy() for card in self.cards]
        return Pile(copied_cards)

    def unselect_cards(self) -> None:
        from widgets.card import Card

        card: Card
        for card in self.cards:
            card.make_unselected()
