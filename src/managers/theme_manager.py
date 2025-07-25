import time

from rich import box
from rich.box import Box
from textual.screen import Screen
from textual.timer import Timer

from widgets.card_holder import CardHolder


class ThemeManager:
    """
    Handles theme switching and animations for the game's UI components.

    This class provides methods to change themes, manage animations, and
    update UI layouts accordingly.
    """

    def __init__(self) -> None:
        self.current_theme = "default"
        self.rainbow_timer: Timer | None = None

    def switch_theme(self, screen: Screen):
        from widgets.card import Card

        match self.current_theme:
            case "default":
                self.current_theme = "ascii"
            case "ascii":
                self.current_theme = "rainbow"
                self.start_rainbow_animation(screen)
            case "rainbow":
                self.current_theme = "default"
                self.stop_rainbow_animation()

        for card in screen.query(Card):
            card.refresh()

        for holder in screen.query(CardHolder):
            holder.refresh()

    def start_rainbow_animation(self, screen: Screen):
        """
        Starts the rainbow animation for the cards.

        Creates dynamic color effects by updating card colors at regular intervals.
        """
        from widgets.card import Card

        self.stop_rainbow_animation()

        start_time = time.time()

        def update_rainbow_colors() -> None:
            if self.current_theme == "rainbow":
                cards = list(screen.query(Card))
                total_cards = len(cards)

                if total_cards > 0:
                    current_time = time.time()
                    elapsed_time = current_time - start_time

                    wave_speed = 0.2
                    wave_length = 0.2

                    for i, card in enumerate(cards):
                        card_position = i / max(1, total_cards - 1)

                        phase = (
                            elapsed_time * wave_speed + card_position * wave_length
                        ) % 1.0

                        card.color = self.get_rainbow_color_with_phase(phase)
                        card.refresh()

        self.rainbow_timer = screen.set_interval(1 / 120, update_rainbow_colors)

    def get_rainbow_color_with_phase(self, phase: float) -> str:
        """
        Calculates a rainbow color based on the provided phase.

        :param phase: A float representing the phase in the color cycle (0.0 to 1.0).
        :return: A hex color string.
        """
        hue = int(360 * phase)

        saturation = 1.0
        lightness = 0.5

        h = hue / 60
        c = (1 - abs(2 * lightness - 1)) * saturation
        x = c * (1 - abs((h % 2) - 1))
        m = lightness - c / 2

        if 0 <= h < 1:
            r, g, b = c, x, 0
        elif 1 <= h < 2:
            r, g, b = x, c, 0
        elif 2 <= h < 3:
            r, g, b = 0, c, x
        elif 3 <= h < 4:
            r, g, b = 0, x, c
        elif 4 <= h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        r, g, b = [int((val + m) * 255) for val in (r, g, b)]

        return f"#{r:02x}{g:02x}{b:02x}"

    def stop_rainbow_animation(self) -> None:
        if self.rainbow_timer:
            self.rainbow_timer.stop()
            self.rainbow_timer = None

    def get_box(self) -> Box | None:
        match self.current_theme:
            case "default" | "rainbow":
                return box.ROUNDED
            case "ascii":
                return box.ASCII
        return None

    def get_selected_box(self) -> Box | None:
        match self.current_theme:
            case "default" | "rainbow":
                return box.HEAVY
            case "ascii":
                return box.HEAVY
        return None