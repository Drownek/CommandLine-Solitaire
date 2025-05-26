from __future__ import annotations

from typing import cast, TYPE_CHECKING, Iterator

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
        depending on the current state of the game.
        """
        from screens.game import Game

        # Handle stash card display
        yield self._prepare_stash_card_for_display()

        # Handle waste cards display based on game mode
        game: Game = cast(Game, self.screen)

        if game.easy_mode:
            yield self._prepare_easy_mode_waste_display()
        else:
            yield from self._prepare_standard_waste_display()

    def _prepare_stash_card_for_display(self) -> Card:
        """Prepare and position the stash card for display."""
        from widgets.card import Card

        top_stash_card = self.get_top_stash_card()

        if top_stash_card:
            top_stash_card.offset = (0, 0)  # type: ignore
            return top_stash_card

        return Card(" ", "⟳")  # Return refresh symbol when stash is empty

    def _prepare_easy_mode_waste_display(self) -> Card | CardHolder:
        """Prepare waste display for easy mode (only top card)."""
        top_waste_card = self.get_top_waste_card()

        if top_waste_card:
            top_waste_card.offset = (0, 0)  # type: ignore
            return top_waste_card

        return CardHolder()  # Empty placeholder when no waste card is available

    def _prepare_standard_waste_display(self) -> Iterator[Card | CardHolder]:
        """Prepare waste display for standard mode (showing up to three cards)."""
        if not self.waste:
            yield CardHolder()
            return

        # Display the last three cards with offset positioning
        visible_waste_cards = self.waste[-3:]
        for index, card in enumerate(visible_waste_cards):
            card.offset = (index * -4, 0)  # type: ignore
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
