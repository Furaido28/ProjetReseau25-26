import sqlite3
import bcrypt
from pathlib import Path

class SecurityManager:
    """
    Gère le mot de passe global + initialise/maintient le schéma SQLite.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._ensure_schema()  # ✅ crée/upgrade les tables si besoin

    def _ensure_schema(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            password BLOB NOT NULL
        );

        CREATE TABLE IF NOT EXISTS decoupes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            responsable TEXT NOT NULL,
            base_ip TEXT NOT NULL,
            base_mask TEXT NOT NULL,
            mode TEXT NOT NULL,
            value INT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_decoupes_responsable ON decoupes(responsable);
        """)
        self.conn.commit()

        # Petit log de debug à côté de la DB pour vérifier le schéma en prod
        try:
            tables = [r[0] for r in self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1"
            ).fetchall()]
            Path(self.db_path).with_suffix(".log").write_text(
                f"DB: {self.db_path}\nTables: {tables}\n"
            )
        except Exception:
            pass

    # ---------- Mot de passe ----------
    def has_password(self) -> bool:
        self.cursor.execute("SELECT 1 FROM settings WHERE id = 1")
        return self.cursor.fetchone() is not None

    def set_password(self, plain_password: str):
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        self.cursor.execute("DELETE FROM settings")
        self.cursor.execute(
            "INSERT INTO settings (id, password) VALUES (1, ?)", (hashed,)
        )
        self.conn.commit()

    def verify_password(self, plain_password: str) -> bool:
        self.cursor.execute("SELECT password FROM settings WHERE id = 1")
        row = self.cursor.fetchone()
        if not row:
            return False
        stored = row["password"]
        if isinstance(stored, str):  # compat ancien schéma TEXT
            stored = stored.encode("utf-8")
        return bcrypt.checkpw(plain_password.encode(), stored)

    def close(self):
        self.conn.close()