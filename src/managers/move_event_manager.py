from pygame.mixer import Sound
from textual.screen import Screen

from controllers.service_locator import ServiceLocator
from managers.game_state_manager import GameStateManager


class MoveEventManager:

    def __init__(self, game_state_manager: GameStateManager = None):
        self._game_state_manager = game_state_manager or ServiceLocator.get(GameStateManager)

    def on_post_move_event(self, screen: Screen) -> None:
        """Used for checking if game is won, and move count tracker"""
        from pasjans import GameHeader
        from widgets.foundation import Foundation
        from widgets.card import Card
        from widgets.winner_message import WinnerMessage

        Sound("sounds/flip.ogg").play()

        game_header: GameHeader = screen.query_one(GameHeader)
        game_header.moves += 1

        king_card_in_foundation_count = 0
        foundation: Foundation = screen.query_one(Foundation)

        card: Card | None
        for card in foundation.cards:
            if card is not None and card.value == "K":
                king_card_in_foundation_count += 1

        if king_card_in_foundation_count == 4:
            winner_message: WinnerMessage = screen.query_one(WinnerMessage)
            winner_message.show(game_header.moves)

    def on_pre_move_event(self, screen: Screen) -> None:
        """Used for tracking moves for undo operation"""
        from widgets.foundation import Foundation
        from widgets.tableau import Tableau
        from widgets.stash_waste import StashWaste
        from managers.game_state_manager import GameState

        foundation: Foundation = screen.query_one(Foundation)
        tableau: Tableau = screen.query_one(Tableau)
        stash_waste: StashWaste = screen.query_one(StashWaste)
        state = GameState(
            [pile.deep_copy() for pile in tableau.piles],
            stash_waste.deep_copy_stash(),
            stash_waste.deep_copy_waste(),
            foundation.copy_cards()
        )
        self._game_state_manager.previous_states.append(state)