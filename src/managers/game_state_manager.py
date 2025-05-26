from __future__ import annotations

from textual.screen import Screen

from widgets.card import Card
from widgets.foundation import Foundation
from widgets.stash_waste import StashWaste
from widgets.tableau import Pile, Tableau


class GameStateManager:
    """
    Manages the game state by allowing operations such as undoing the last move.

    This class provides functionality to restore the game to a previous state
    by managing a stack of game states. It interacts with components such as
    the foundation, tableau, stash, and waste piles to enable reverting changes
    made during gameplay.
    """

    def __init__(self) -> None:
        self.previous_states: list[GameState] = []

    def undo_last_operation(self, screen: Screen) -> None:
        """
        Undo the last operation performed during the game.

        This method reverts the game state to the most recent one stored in the
        `previous_states` stack. It also updates the number of moves performed
        and checks for undo limits. The affected components include the foundation,
        tableau, stash, and waste piles.
        """
        from pasjans import GameHeader

        foundation: Foundation = screen.query_one(Foundation)
        tableau: Tableau = screen.query_one(Tableau)
        stash_waste: StashWaste = screen.query_one(StashWaste)
        game_header = screen.query_one(GameHeader)

        if not self.previous_states:
            screen.notify("No more actions to undo.")
            return

        if game_header.remaining_undo <= 0:
            screen.notify("Undo limit reached.")
            return

        game_header.moves -= 1
        game_header.remaining_undo -= 1
        previous_game_state: GameState = self.previous_states.pop()

        foundation.cards = previous_game_state.foundation.copy()
        tableau.piles = previous_game_state.piles.copy()
        pile: Pile
        card: Card
        for pile in tableau.piles:
            for card in pile.cards:
                card.refresh()
        stash_waste.stash = previous_game_state.stash.copy()
        for card in stash_waste.stash:
            card.refresh()
        stash_waste.waste = previous_game_state.waste.copy()
        for card in stash_waste.waste:
            card.refresh()

        # Make all cards unselected
        for pile in tableau.piles:
            for card in pile.cards:
                card.make_unselected()
        for card in stash_waste.stash:
            card.make_unselected()
        for card in stash_waste.waste:
            card.make_unselected()


class GameState:
    """
    Represents the current state of the game, including UI and card components.

    This class provides a snapshot of the current game by storing references to
    the screen, piles in the tableau, the stash, waste piles, and the foundation.
    It enables restoring the game state during an undo operation.

    :ivar piles: A list of `Pile` objects representing tableau cards in the game.
    :ivar stash: A list of `Card` objects representing the current stash in the game.
    :ivar waste: A list of `Card` objects representing the waste pile in the game.
    :ivar foundation: A list of `Card` objects or None for representing the state
        of the foundation.
    """

    def __init__(
        self,
        piles: list[Pile],
        stash: list[Card],
        waste: list[Card],
        foundation: list[Card | None],
    ):
        self.piles = piles
        self.stash = stash
        self.waste = waste
        self.foundation = foundation

