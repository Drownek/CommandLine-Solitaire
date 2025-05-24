from __future__ import annotations

from typing import cast, TYPE_CHECKING

from rich.panel import Panel
from textual.css.query import DOMQuery
from textual.widget import Widget

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
        return Panel.fit(
            "    ",
            border_style="dim",
            style="dim",
            box=ThemeManager.get_box(),
        )

    def on_click(self) -> None:
        """
        Handle the click event for a game card interaction. This method manages the logic for
        moving cards between piles, waste, and foundation during the game. Depending on the
        selected cards and their respective piles, it decides how cards should be moved or
        whether a valid operation is being performed. It also handles specific rules for
        moving cards such as placing only a king on an empty pile or only an ace on an
        empty foundation.
        """

        from widgets.tableau import Pile
        from widgets.stash_waste import StashWaste
        from pasjans import Game
        from widgets.foundation import Foundation
        from widgets.card import Card

        selected_cards = cast(DOMQuery[Card], self.screen.query("Card.selected"))

        if not selected_cards:
            return

        selected_card: Card = selected_cards[0]
        holder_pile: Pile | None = self.pile
        selected_card_pile: Pile | None = selected_card.get_pile()
        stash_waste: StashWaste = self.screen.query_one(StashWaste)

        # If holder is invisible one to make ability to put K
        if holder_pile:
            if selected_card.value == 'K':
                # Moving card from tableau
                if selected_card_pile:
                    Game.on_pre_move_event(self.screen)

                    selected_pile_cards: list[Card] = selected_card_pile.cards.copy()
                    card: Card
                    for card in selected_cards:
                        selected_pile_cards.remove(card)

                    if selected_pile_cards:
                        selected_pile_cards[-1].unhide()

                    selected_card_pile.cards = selected_pile_cards

                    holder_pile_cards: list[Card] = holder_pile.cards.copy()
                    for card in selected_cards:
                        card.make_unselected()
                        holder_pile_cards.append(card)

                    holder_pile.cards = holder_pile_cards

                    Game.on_post_move_event(self.screen)
                # Moving card from waste
                elif selected_card in stash_waste.waste:
                    Game.on_pre_move_event(self.screen)

                    waste_cards: list[Card] = stash_waste.waste.copy()
                    waste_cards.remove(selected_card)
                    stash_waste.waste = waste_cards
                    if waste_cards:
                        waste_cards[-1].refresh()

                    holder_pile_cards = holder_pile.cards.copy()
                    holder_pile_cards.append(selected_card)
                    selected_card.make_unselected()
                    holder_pile.cards = holder_pile_cards

                    Game.on_post_move_event(self.screen)
            return

        # Card holders are only at foundation, waste, so dont allow more than 1 card to move
        if len(selected_cards) != 1:
            return

        foundation = self.screen.query_one(Foundation)

        # If holder belong to foundation
        if self.foundation_index is not None:
            if selected_card.value == 'A':
                # From pile to foundation
                if selected_card_pile:
                    Game.on_pre_move_event(self.screen)

                    selected_pile_cards = selected_card_pile.cards.copy()
                    selected_pile_cards.remove(selected_card)
                    selected_card.make_unselected()

                    foundation_cards = foundation.cards.copy()
                    foundation_cards[self.foundation_index] = selected_card
                    foundation.cards = foundation_cards

                    if selected_pile_cards:
                        selected_pile_cards[-1].unhide()

                    selected_card_pile.cards = selected_pile_cards

                    Game.on_post_move_event(self.screen)
                # From waste to foundation
                elif selected_card in stash_waste.waste:
                    Game.on_pre_move_event(self.screen)

                    waste_cards = stash_waste.waste.copy()
                    waste_cards.remove(selected_card)
                    selected_card.make_unselected()
                    stash_waste.waste = waste_cards
                    if waste_cards:
                        waste_cards[-1].refresh()

                    foundation = self.screen.query_one(Foundation)
                    foundation_cards = foundation.cards.copy()
                    foundation_cards[self.foundation_index] = selected_card
                    foundation.cards = foundation_cards

                    Game.on_post_move_event(self.screen)
