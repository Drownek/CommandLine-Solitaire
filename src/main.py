"""
This module serves as the entry point for the Pasjans card game application.
It initializes the game and starts the main application loop.
"""
from typing import NoReturn

from pasjans import Pasjans


def main() -> NoReturn:
    try:
        game = Pasjans()
        game.run()
    except Exception as e:
        print(f"Error running Pasjans: {e}")
        raise


if __name__ == "__main__":
    main()
