from __future__ import annotations

from typing import cast, TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive

from widgets.card_holder import CardHolder

if TYPE_CHECKING:
    from widgets.card import Card


class StashWaste(HorizontalGroup):
    """
    Represents a group of card stacks, including a stash and a waste pile, for managing
    and rendering cards within a game. Provides mechanisms for card arrangement, copying,
    and selection handling.

    This class is designed to visually and functionally manage a stash and waste pile of
    cards. It allows rendering the top cards of both piles, handles card selection
    state, and supports deep copying for both stash and waste piles.

    :ivar stash: The list of cards in the stash pile.
    :ivar waste: The list of cards in the waste pile.
    """

    stash = reactive([], recompose=True)  # type: ignore
    waste = reactive([], recompose=True)  # type: ignore

    def __init__(self, stash: list[Card]):
        super().__init__()
        self.stash = stash
        self.waste = []

    def compose(self) -> ComposeResult:
        """
        Compose cards for display, including cards from the stash, waste, and appropriate placeholders.

        This function is responsible for yielding a sequence of cards or placeholders to be displayed,
        depending on the current state of the game. If a card exists at the top of the stash, or if the
        game is in easy mode, it handles the respective card offset adjustments and yields the resulting
        cards or placeholders. For non-easy mode, it processes the last three cards in the waste pile
        (scaled down if fewer cards are present) and adjusts their offsets according to their position.
        """
        from screens.game import Game
        from widgets.card import Card

        top_stash_card: Card | None = self.get_top_stash_card()
        if top_stash_card:
            top_stash_card.offset = (0, 0)  # type: ignore

        yield top_stash_card or Card(" ", "⟳")
        game: Game = cast(Game, self.screen)
        if game.easy_mode:
            top_waste_card = self.get_top_waste_card()
            if top_waste_card:
                top_waste_card.offset = (0, 0)  # type: ignore
            yield top_waste_card or CardHolder()
        else:
            if not self.waste:
                yield CardHolder()
                return

            last_cards = self.waste[-3:]

            for i, card in enumerate(last_cards):
                card.offset = (i * -4, 0)  # type: ignore
                yield card

    def get_top_stash_card(self) -> Card | None:
        return self.stash[-1] if self.stash else None

    def get_top_waste_card(self) -> Card | None:
        return self.waste[-1] if self.waste else None

    def deep_copy_stash(self) -> list[Card]:
        copied_cards = [card.copy() for card in self.stash]
        return copied_cards

    def deep_copy_waste(self) -> list[Card]:
        copied_cards = [card.copy() for card in self.waste]
        return copied_cards

    def unselect_all_cards(self) -> None:
        for card in self.stash:
            card.make_unselected()
        for card in self.waste:
            card.make_unselected()
