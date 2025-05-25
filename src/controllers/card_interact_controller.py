from __future__ import annotations

from random import shuffle
from typing import cast, TYPE_CHECKING

from textual.css.query import DOMQuery
from textual.screen import Screen

import constants

if TYPE_CHECKING:
    from pasjans import Game
    from widgets.card import Card
    from widgets.tableau import Pile
    from widgets.foundation import Foundation
    from widgets.stash_waste import StashWaste
    from widgets.card_holder import CardHolder


class CardInteractController:
    """
    Controller for card interactions in the game.
    
    This class handles all the logic related to card interactions, such as clicking on cards,
    moving cards between piles, and handling game state changes. It separates the game logic
    from the UI components.
    """
    
    def __init__(self, screen: Screen, easy_mode: bool):
        """
        Initialize the card interaction controller.
        
        Args:
            screen: The game screen
            easy_mode: Whether the game is in easy mode
        """
        self.screen = screen
        self.easy_mode = easy_mode
    
    def handle_card_click(self, card: Card) -> None:
        """
        Handle a click on a card.
        
        This method determines what action to take based on the card that was clicked
        and the current game state.
        
        Args:
            card: The card that was clicked
        """

        from widgets.stash_waste import StashWaste
        from widgets.tableau import Pile
        from widgets.card import Card
        from pasjans import Game
        from widgets.foundation import Foundation

        stash_waste: StashWaste = self.screen.query_one(StashWaste)
        top_stash_card = stash_waste.get_top_stash_card()
        game: Game = cast(Game, self.screen)

        # Discovering new card from stash
        if top_stash_card == card:
            self._handle_stash_card_draw(stash_waste, game)
            return

        # Rerolling cards if reached end of stash
        elif top_stash_card is None and card.value == "⟳":
            self._handle_stash_reroll(stash_waste)
            return

        # For rest we dont want to be able to click on hidden cards
        if card.hidden:
            return

        pile: Pile | None = card.get_pile()
        selected_cards: DOMQuery[Card] = cast(DOMQuery[Card], self.screen.query("Card.selected"))

        # Clicked card belong to pile
        if pile:
            self._handle_pile_card_click(pile, selected_cards, stash_waste, card)
            return

        foundation: Foundation = self.screen.query_one(Foundation)

        # Moving to foundation
        if card in foundation.cards:
            self._handle_foundation_card_click(foundation, selected_cards, stash_waste, card)
            return

        # Allow selecting cards in waste
        if card in stash_waste.waste:
            self._handle_waste_card_click(stash_waste, game, card)
    
    def _handle_stash_card_draw(self, stash_waste: StashWaste, game: Game) -> None:
        """Handle drawing a card from the stash."""
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
            card = stash[-1]
            waste.append(card)
            stash.pop()
            card.unhide()
        
        stash_waste.waste = waste
        stash_waste.stash = stash
        
        Game.on_post_move_event(self.screen)
    
    def _handle_stash_reroll(self, stash_waste: StashWaste) -> None:
        """Handle rerolling the stash when it's empty."""
        from pasjans import Game
        
        Game.on_pre_move_event(self.screen)
        
        waste = stash_waste.waste.copy()
        shuffle(waste)
        for card in waste:
            card.hide()
        stash_waste.waste = []
        stash_waste.stash = waste
        
        Game.on_post_move_event(self.screen)
    
    def _handle_pile_card_click(self, pile: Pile, selected_cards: DOMQuery[Card], 
                               stash_waste: StashWaste, card: Card) -> None:
        """Handle clicking on a card in a pile."""
        from widgets.card import Card

        if card.is_selected():
            pile.unselect_cards()
        else:
            top_card: Card = pile.cards[-1]

            # Moving from pile
            if selected_cards and top_card == card:
                self._handle_move_to_pile(pile, selected_cards, stash_waste)
            # Not moving from pile
            else:
                self._select_cards_in_pile(pile, stash_waste, card)
    
    def _handle_move_to_pile(self, pile: Pile, selected_cards: DOMQuery[Card], 
                            stash_waste: StashWaste) -> None:
        """Handle moving cards to a pile."""
        from pasjans import Game
        from widgets.card import Card

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
        """Check if moving a card to a pile is valid."""
        # Check card colors (red on black, black on red)
        if ((top_card.suit in constants.RED_SUITS and bottom_card.suit in constants.RED_SUITS) or
                (top_card.suit in constants.BLACK_SUITS and bottom_card.suit in constants.BLACK_SUITS)):
            return False
        
        # Check card values (decreasing sequence)
        if constants.VALUES.index(bottom_card.value) != constants.VALUES.index(top_card.value) - 1:
            return False
        
        return True
    
    def _move_from_pile_to_pile(self, source_pile: Pile, selected_cards: DOMQuery[Card]) -> None:
        """Handle moving cards from one pile to another."""
        source_pile_cards = source_pile.cards.copy()
        for card in selected_cards:
            source_pile_cards.remove(card)
        if source_pile_cards:
            source_pile_cards[-1].unhide()
        
        source_pile.cards = source_pile_cards
    
    def _move_from_waste_to_pile(self, stash_waste: StashWaste, card: Card) -> None:
        """Handle moving a card from waste to a pile."""
        waste_cards = stash_waste.waste.copy()
        waste_cards.remove(card)
        stash_waste.waste = waste_cards
        if waste_cards:
            waste_cards[-1].refresh()
    
    def _select_cards_in_pile(self, pile: Pile, stash_waste: StashWaste, clicked_card: Card) -> None:
        """Handle selecting cards in a pile."""
        from widgets.tableau import Pile
        
        # Unselect all cards
        for current_pile in self.screen.query(Pile):
            current_pile.unselect_cards()
        
        stash_waste.unselect_all_cards()
        
        # Select all cards from selected to top
        index = pile.cards.index(clicked_card)
        card: Card
        for card in pile.cards[index:]:
            if not card.is_selected():
                card.make_selected()
    
    def _handle_foundation_card_click(self, foundation: Foundation, selected_cards: DOMQuery[Card], 
                                     stash_waste: StashWaste, clicked_card: Card) -> None:
        """Handle clicking on a card in the foundation."""
        if len(selected_cards) != 1:
            return
        
        bottom_card = selected_cards[0]
        
        if not self._is_valid_foundation_move(clicked_card, bottom_card):
            return
            
        selected_card_pile = bottom_card.get_pile()
        
        # Pile to foundation
        if selected_card_pile:
            self._move_from_pile_to_foundation(selected_card_pile, foundation, bottom_card, clicked_card)
        # Waste to foundation
        elif bottom_card in stash_waste.waste:
            self._move_from_waste_to_foundation(stash_waste, foundation, bottom_card, clicked_card)

    def _is_valid_foundation_move(self, foundation_card: Card, card_to_move: Card) -> bool:
        """Check if moving a card to the foundation is valid."""
        if card_to_move.suit != foundation_card.suit:
            return False

        current_value_index = constants.VALUES.index(foundation_card.value)
        next_value_index = constants.VALUES.index(card_to_move.value)

        if next_value_index != current_value_index + 1:
            return False

        return True

    def _move_from_pile_to_foundation(self, pile: Pile, foundation: Foundation,
                                     card: Card, foundation_card: Card) -> None:
        """Handle moving a card from a pile to the foundation."""
        from pasjans import Game

        Game.on_pre_move_event(self.screen)

        pile_cards = pile.cards.copy()
        pile_cards.remove(card)

        foundation_cards: list[Card | None] = foundation.cards.copy()
        foundation_cards[foundation_cards.index(foundation_card)] = card
        foundation.cards = foundation_cards
        
        card.make_unselected()
        
        if pile_cards:
            pile_cards[-1].unhide()
        
        pile.cards = pile_cards
        
        Game.on_post_move_event(self.screen)
    
    def _move_from_waste_to_foundation(self, stash_waste: StashWaste, foundation: Foundation, 
                                      card: Card, foundation_card: Card) -> None:
        """Handle moving a card from waste to the foundation."""
        from pasjans import Game
        
        Game.on_pre_move_event(self.screen)
        
        waste_cards = stash_waste.waste.copy()
        waste_cards.remove(card)
        stash_waste.waste = waste_cards
        if waste_cards:
            waste_cards[-1].refresh()
        
        foundation_cards: list[Card | None] = foundation.cards.copy()
        foundation_cards[foundation_cards.index(foundation_card)] = card
        foundation.cards = foundation_cards
        
        card.make_unselected()
        
        Game.on_post_move_event(self.screen)
    
    def _handle_waste_card_click(self, stash_waste: StashWaste, game: Game, card: Card) -> None:
        """Handle clicking on a card in the waste."""
        from widgets.tableau import Pile
        
        if card.is_selected():
            card.make_unselected()
        else:
            # Check if card is top one from waste if on hard mode
            top_waste_card = stash_waste.get_top_waste_card()
            if game.easy_mode or top_waste_card == card:
                # Unselect all pile cards
                for pile in self.screen.query(Pile):
                    pile.unselect_cards()

                card.make_selected()

    def handle_card_holder_click(self, card_holder: CardHolder) -> None:
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
        holder_pile: Pile | None = card_holder.pile
        selected_card_pile: Pile | None = selected_card.get_pile()
        stash_waste: StashWaste = self.screen.query_one(StashWaste)

        # If holder is invisible one to make ability to put K
        if holder_pile:
            if selected_card.value == "K":
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
        if card_holder.foundation_index is not None:
            if selected_card.value == "A":
                # From pile to foundation
                if selected_card_pile:
                    Game.on_pre_move_event(self.screen)

                    selected_pile_cards = selected_card_pile.cards.copy()
                    selected_pile_cards.remove(selected_card)
                    selected_card.make_unselected()

                    foundation_cards = foundation.cards.copy()
                    foundation_cards[card_holder.foundation_index] = selected_card
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
                    foundation_cards[card_holder.foundation_index] = selected_card
                    foundation.cards = foundation_cards

                    Game.on_post_move_event(self.screen)
