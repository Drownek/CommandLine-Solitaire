from __future__ import annotations

from random import shuffle
from typing import cast, TYPE_CHECKING

from rich.panel import Panel
from textual.css.query import DOMQuery
from textual.reactive import reactive
from textual.widget import Widget

import constants
from managers.theme_manager import ThemeManager

if TYPE_CHECKING:
    from widgets.tableau import Pile


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

    def __init__(self, suit: str, value: str, hidden: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.suit = suit
        self.value = value
        self.hidden = hidden

    def __str__(self):
        return f"{self.suit}{self.value}"

    def __repr__(self):
        return f"{self.suit}{self.value}"

    def copy(self) -> Card:
        return Card(self.suit, self.value, self.hidden)

    def render(self) -> Panel:
        red = self.suit in ('♥', '♦')
        if self.hidden:
            self.color = "dim"
        elif ThemeManager.current_theme != "rainbow":
            self.color = "red" if red else "white"

        value: str = self.value if not self.hidden else '?'
        symbol_display = self.suit if not self.hidden else '?'

        spaces = "   " if len(value) == 2 else "    "
        content = f"[{self.color}]{symbol_display}{value}[/][{self.color}][/]{spaces}\n\n\n"

        if self.is_selected():
            border_box = ThemeManager.get_selected_box()
        else:
            border_box = ThemeManager.get_box()

        return Panel.fit(
            content,
            border_style=self.color,
            box=border_box,
            padding=(0, 0),
            title_align="left"
        )

    def on_click(self) -> None:
        from pasjans import Game
        from widgets.tableau import Pile
        from widgets.stash_waste import StashWaste
        from widgets.foundation import Foundation

        stash_waste: StashWaste = self.screen.query_one(StashWaste)
        top_stash_card = stash_waste.get_top_stash_card()
        game: Game = cast(Game, self.screen)

        # Discovering new card from stash
        if top_stash_card == self:
            self._handle_stash_card_draw(stash_waste, game)
            return

        # Rerolling cards if reached end of stash
        elif top_stash_card is None and self.value == "⟳":
            self._handle_stash_reroll(stash_waste)
            return

        # For rest we dont want to be able to click on hidden cards
        if self.hidden:
            return

        pile: Pile | None = self.get_pile()
        selected_cards: DOMQuery[Card] = cast(DOMQuery[Card], self.screen.query("Card.selected"))

        # Clicked card belong to pile
        if pile:
            self._handle_pile_card_click(pile, selected_cards, stash_waste)
            return

        foundation: Foundation = self.screen.query_one(Foundation)

        # Moving to foundation
        if self in foundation.cards:
            self._handle_foundation_card_click(foundation, selected_cards, stash_waste)
            return

        # Allow selecting cards in waste
        if self in stash_waste.waste:
            self._handle_waste_card_click(stash_waste, game)

    def _handle_stash_card_draw(self, stash_waste, game) -> None:
        from pasjans import Game

        Game.on_pre_move_event(self.screen)

        for card in stash_waste.waste:
            card.make_unselected()

        waste = stash_waste.waste.copy()
        stash = stash_waste.stash.copy()

        if not game.easy_mode:
            cards_to_pop = min(3, len(stash))
            for _ in range(cards_to_pop):
                if stash:
                    card = stash.pop()
                    card.unhide()
                    waste.append(card)
        else:
            waste.append(self)
            stash.pop()
            self.unhide()

        stash_waste.waste = waste
        stash_waste.stash = stash

        Game.on_post_move_event(self.screen)

    def _handle_stash_reroll(self, stash_waste) -> None:
        from pasjans import Game

        Game.on_pre_move_event(self.screen)

        waste = stash_waste.waste.copy()
        shuffle(waste)
        for card in waste:
            card.hide()
        stash_waste.waste = []
        stash_waste.stash = waste

        Game.on_post_move_event(self.screen)

    def _handle_pile_card_click(self, pile, selected_cards, stash_waste) -> None:
        if self.is_selected():
            pile.unselect_cards()
        else:
            top_card: Card = pile.cards[-1]

            # Moving from pile
            if selected_cards and top_card == self:
                self._handle_move_to_pile(pile, selected_cards, stash_waste)
            # Not moving from pile
            else:
                self._select_cards_in_pile(pile, stash_waste)

    def _handle_move_to_pile(self, pile, selected_cards, stash_waste) -> None:
        from pasjans import Game

        top_card: Card = pile.cards[-1]
        bottom_card: Card = selected_cards[0]

        if not self._is_valid_pile_move(top_card, bottom_card):
            return

        Game.on_pre_move_event(self.screen)

        pile_cards = pile.cards.copy()
        for card in selected_cards:
            pile_cards.append(card.copy())
        pile.cards = pile_cards

        selected_pile = bottom_card.get_pile()

        # Pile to pile
        if selected_pile:
            self._move_from_pile_to_pile(selected_pile, selected_cards)
        # Waste to pile
        elif bottom_card in stash_waste.waste:
            self._move_from_waste_to_pile(stash_waste, bottom_card)

        Game.on_post_move_event(self.screen)

    def _is_valid_pile_move(self, top_card: Card, bottom_card: Card) -> bool:
        # Sprawdź kolory kart (czerwona na czarną, czarna na czerwoną)
        if ((top_card.suit in constants.RED_SUITS and bottom_card.suit in constants.RED_SUITS) or
                (top_card.suit in constants.BLACK_SUITS and bottom_card.suit in constants.BLACK_SUITS)):
            return False

        # Sprawdź wartości kart (sekwencja malejąca)
        if constants.VALUES.index(bottom_card.value) != constants.VALUES.index(top_card.value) - 1:
            return False

        return True

    def _move_from_pile_to_pile(self, source_pile, selected_cards) -> None:
        source_pile_cards = source_pile.cards.copy()
        for card in selected_cards:
            source_pile_cards.remove(card)
        if source_pile_cards:
            source_pile_cards[-1].unhide()

        source_pile.cards = source_pile_cards

    def _move_from_waste_to_pile(self, stash_waste, card) -> None:
        waste_cards = stash_waste.waste.copy()
        waste_cards.remove(card)
        stash_waste.waste = waste_cards
        if waste_cards:
            waste_cards[-1].refresh()

    def _select_cards_in_pile(self, pile, stash_waste) -> None:
        from widgets.tableau import Pile
        
        # Unselect all cards
        for current_pile in self.screen.query(Pile):
            current_pile.unselect_cards()

        stash_waste.unselect_all_cards()

        # Select all cards from selected to top
        index = pile.cards.index(self)
        card: Card
        for card in pile.cards[index:]:
            if not card.is_selected():
                card.make_selected()

    def _handle_foundation_card_click(self, foundation, selected_cards, stash_waste) -> None:
        if len(selected_cards) != 1:
            return

        bottom_card = selected_cards[0]
        
        if not self._is_valid_foundation_move(bottom_card):
            return
            
        selected_card_pile = bottom_card.get_pile()

        # Pile to foundation
        if selected_card_pile:
            self._move_from_pile_to_foundation(selected_card_pile, foundation, bottom_card)
        # Waste to foundation
        elif bottom_card in stash_waste.waste:
            self._move_from_waste_to_foundation(stash_waste, foundation, bottom_card)

    def _is_valid_foundation_move(self, bottom_card: Card) -> bool:
        if bottom_card.suit != self.suit:
            return False

        current_value_index = constants.VALUES.index(self.value)
        next_value_index = constants.VALUES.index(bottom_card.value)

        if next_value_index != current_value_index + 1:
            return False
            
        return True

    def _move_from_pile_to_foundation(self, pile, foundation, card) -> None:
        from pasjans import Game
        
        Game.on_pre_move_event(self.screen)

        pile_cards = pile.cards.copy()
        pile_cards.remove(card)

        foundation_cards: list[Card | None] = foundation.cards.copy()
        foundation_cards[foundation_cards.index(self)] = card
        foundation.cards = foundation_cards

        card.make_unselected()

        if pile_cards:
            pile_cards[-1].unhide()

        pile.cards = pile_cards

        Game.on_post_move_event(self.screen)

    def _move_from_waste_to_foundation(self, stash_waste, foundation, card) -> None:
        from pasjans import Game
        
        Game.on_pre_move_event(self.screen)

        waste_cards = stash_waste.waste.copy()
        waste_cards.remove(card)
        stash_waste.waste = waste_cards
        if waste_cards:
            waste_cards[-1].refresh()

        foundation_cards: list[Card | None] = foundation.cards.copy()  # type: ignore
        foundation_cards[foundation_cards.index(self)] = card
        foundation.cards = foundation_cards

        card.make_unselected()

        Game.on_post_move_event(self.screen)

    def _handle_waste_card_click(self, stash_waste, game) -> None:
        from widgets.tableau import Pile
        
        if self.is_selected():
            self.make_unselected()
        else:
            # Check if card is top one from waste if on hard mode
            top_waste_card = stash_waste.get_top_waste_card()
            if game.easy_mode or top_waste_card == self:
                # Unselect all pile cards
                for pile in self.screen.query(Pile):
                    pile.unselect_cards()

                self.make_selected()

    def hide(self):
        self.hidden = True
        self.refresh()

    def unhide(self):
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
