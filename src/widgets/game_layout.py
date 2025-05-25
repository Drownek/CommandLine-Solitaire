from __future__ import annotations

from random import shuffle

from textual.app import ComposeResult
from textual.containers import VerticalGroup

import constants
from widgets.card import Card
from widgets.tableau import Pile, Tableau
from widgets.top_container import TopContainer


class GameLayout(VerticalGroup):
    """
    Represents the layout of a card game displayed vertically. Responsible for
    initializing the deck, shuffling cards, and organizing them into piles and
    stash for gameplay. This class orchestrates the visual components of the
    game's layout such as tableau and top container.
    """

    def compose(self) -> ComposeResult:
        """Compose the game layout with tableau and stash."""

        # Create and shuffle the deck
        deck = self.create_deck()
        shuffle(deck)

        # Create tableau piles
        tableau_piles = self._create_tableau_piles(deck)

        # Prepare stash with remaining cards
        remaining_cards = self._prepare_stash(deck)

        yield TopContainer(remaining_cards)
        yield Tableau(tableau_piles)

    def _create_tableau_piles(
        self, deck: list[Card], pile_count: int = 7
    ) -> list[Pile]:
        """Create tableau piles with cards distributed according to solitaire rules.

        Args:
            deck: The deck of cards to distribute from
            pile_count: Number of piles to create

        Returns:
            List of tableau piles with cards distributed
        """
        piles: list[Pile] = []

        for pile_index in range(pile_count):
            cards_for_pile: list[Card] = []
            cards_in_pile = pile_index + 1

            for card_index in range(cards_in_pile):
                card = deck.pop()
                # Only the top card in each pile is visible
                if card_index != pile_index:
                    card.hide()
                cards_for_pile.append(card)

            pile = Pile()
            pile.cards = cards_for_pile
            piles.append(pile)

        return piles

    def _prepare_stash(self, deck: list[Card]) -> list[Card]:
        """Prepare the stash with remaining cards from the deck.

        Args:
            deck: The remaining cards after tableau distribution

        Returns:
            The prepared stash with all cards hidden
        """
        for card in deck:
            card.hide()
        return deck

    @staticmethod
    def create_deck() -> list[Card]:
        deck = []
        for suit in constants.SUITS:
            for value in constants.VALUES:
                deck.append(Card(suit, value))
        return deck