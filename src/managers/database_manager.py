import sqlite3
from pathlib import Path
from sqlite3 import Connection
from typing import List, Tuple

# Path to the SQLite database file where scores will be stored.
DB_PATH = Path.home() / ".pasjans_scores.db"

# SQL query to create the `scores` table if it doesn't already exist.
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL,
    moves INTEGER NOT NULL,
    time_seconds INTEGER NOT NULL,
    date_played TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);
"""

# SQL query to insert a new score record into the `scores` table.
INSERT_SCORE_SQL = """
INSERT INTO scores (player_name, moves, time_seconds)
VALUES (?, ?, ?);
"""

# SQL query to fetch the top scores from the database, ordered by moves and time.
SELECT_TOP_SCORES_SQL = """
SELECT player_name, moves, time_seconds, date_played
FROM scores
ORDER BY moves ASC, time_seconds ASC
LIMIT ?;
"""


class DatabaseManager:
    """
    A class to manage interactions with the SQLite database for storing and retrieving game scores.

    :param db_path: The file path to the SQLite database. Defaults to `DB_PATH`.
    """

    def __init__(self, db_path: Path = DB_PATH):
        """
        Initialize the DatabaseManager and ensure the scores table exists.

        :param db_path: The file path to the SQLite database. Defaults to `DB_PATH`.
        """
        self.db_path = db_path
        self._ensure_db()

    def _connect(self) -> Connection:
        """
        Establish a connection to the SQLite database.

        :return: A connection object for the database.
        """
        return sqlite3.connect(self.db_path)

    def _ensure_db(self) -> None:
        """
        Ensure the `scores` table exists in the database. If it does not exist, it will be created.
        """
        with self._connect() as conn:
            conn.execute(CREATE_TABLE_SQL)
            conn.commit()

    def save_score(self, player_name: str, moves: int, time_seconds: float) -> None:
        """
        Save a new game score to the database.

        :param player_name: The name of the player.
        :param moves: The number of moves the player took.
        :param time_seconds: The time the player took to finish, in seconds.
        """
        with self._connect() as conn:
            conn.execute(INSERT_SCORE_SQL, (player_name, moves, time_seconds))
            conn.commit()

    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int, int, str]]:
        """
        Retrieve the top scores from the database, ordered by moves and time.

        :param limit: The maximum number of scores to retrieve. Defaults to 10.
        :return: A list of tuples containing (player_name, moves, time_seconds, date_played).
        """
        with self._connect() as conn:
            cursor = conn.execute(SELECT_TOP_SCORES_SQL, (limit,))
            return cursor.fetchall()