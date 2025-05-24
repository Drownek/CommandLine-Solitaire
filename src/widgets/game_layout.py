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
        deck: list[Card] = self.create_deck()
        shuffle(deck)
        piles: list[Pile] = []

        for i in range(7):
            cards: list[Card] = []

            for j in range(i + 1):
                card = deck.pop()
                if j != i:
                    card.hide()
                cards.append(card)

            pile = Pile()
            pile.cards = cards
            piles.append(pile)

        stash: list[Card] = deck
        for card in stash:
            card.hide()

        yield TopContainer(stash)
        yield Tableau(piles)

    @staticmethod
    def create_deck() -> list[Card]:
        deck = []
        for suit in constants.SUITS:
            for value in constants.VALUES:
                deck.append(Card(suit, value))
        return deck
