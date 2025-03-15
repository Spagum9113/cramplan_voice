import sqlite3
from typing import Optional, List
from dataclasses import dataclass
from contextlib import contextmanager
from datetime import datetime

# Dataclass for an interaction


@dataclass
class Interaction:
    id: Optional[int]  # None for new entries
    page: str         # Current page/context (e.g., URL or content)
    user_input: str   # What user said (text from STT or placeholder)
    ai_output: str    # What AI replied (text from OpenAI)
    timestamp: str    # When it happened


class DBDriver:
    def __init__(self, db_name="agent_history.db"):
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def get_connection(self):
        """Handle DB connection with context manager."""
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        """Create interactions table if it doesn't exist."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page TEXT NOT NULL,
                    user_input TEXT NOT NULL,
                    ai_output TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()

    def log_interaction(self, page: str, user_input: str, ai_output: str) -> int:
        """Log a voice interaction and return its ID."""
        timestamp = datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO interactions (page, user_input, ai_output, timestamp) VALUES (?, ?, ?, ?)",
                (page, user_input, ai_output, timestamp)
            )
            conn.commit()
            return cursor.lastrowid

    def get_interaction(self, interaction_id: int) -> Optional[Interaction]:
        """Fetch a single interaction by ID."""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT id, page, user_input, ai_output, timestamp FROM interactions WHERE id = ?",
                (interaction_id,)
            )
            row = cursor.fetchone()
            if row:
                return Interaction(id=row[0], page=row[1], user_input=row[2], ai_output=row[3], timestamp=row[4])
            return None

    def get_history(self, page: Optional[str] = None) -> List[Interaction]:
        """Fetch all interactions, or filter by page."""
        with self.get_connection() as conn:
            if page:
                cursor = conn.execute(
                    "SELECT id, page, user_input, ai_output, timestamp FROM interactions WHERE page = ? ORDER BY timestamp",
                    (page,)
                )
            else:
                cursor = conn.execute(
                    "SELECT id, page, user_input, ai_output, timestamp FROM interactions ORDER BY timestamp"
                )
            rows = cursor.fetchall()
            return [Interaction(id=r[0], page=r[1], user_input=r[2], ai_output=r[3], timestamp=r[4]) for r in rows]

    def print_all_interactions(self):
        """Print all interactions in a readable format"""
        interactions = self.get_history()
        if not interactions:
            print("No interactions found in database.")
            return

        print("\n=== ALL INTERACTIONS ===")
        for interaction in interactions:
            print(f"""
Page: {interaction.page}
User: {interaction.user_input}
AI: {interaction.ai_output}
Time: {interaction.timestamp}
{'='*50}""")


# Test it
if __name__ == "__main__":
    db = DBDriver()
    db.log_interaction("home.html", "What's this?", "It's the homepage!")
    db.print_all_interactions()
