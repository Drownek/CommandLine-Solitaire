from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.reactive import reactive

from widgets.card import Card
from widgets.foundation import Foundation
from widgets.stash_waste import StashWaste


class TopContainer(HorizontalGroup):
    """
    Represents a container that manages horizontal groups and organizes components such
    as a stash and a foundation. This class is designed to serve as a layout container
    that arranges subcomponents efficiently.

    This class allows interaction with and management of card elements, where `stash` is the
    main storage of cards, and components are dynamically composed using the `compose` method.

    :ivar stash: Reactive list that stores cards with recompose functionality.
    """

    stash = reactive([], recompose=True)  # type: ignore

    def __init__(self, stash: list[Card]):
        super().__init__()
        self.stash = stash

    def compose(self) -> ComposeResult:
        yield StashWaste(self.stash)
        yield Foundation()
