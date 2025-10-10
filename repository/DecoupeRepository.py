# repository/DecoupeRepository.py
import sqlite3
from typing import Iterable, Dict, Optional

from pathlib import Path
import sys

class DecoupeRepository:
    def __init__(self, db_path: str = None):
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        if db_path is None:
            self.db_path = (base_dir / ".." / "bdd" / "projetReseau.db").resolve()
        else:
            self.db_path = Path(db_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self):
        conn = sqlite3.connect(str(self.db_path), timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # --- NOUVELLE METHODE SANS OBJET -----------------------------------------
    def insert_decoupe(
        self,
        *,
        name: str,
        responsable: Optional[str],
        base_ip: str,
        base_mask: str,
        mode: str,
        value: str
    ) -> int:
        """Insère une découpe à partir de champs simples et renvoie son id SQLite."""
        sql = """
        INSERT INTO decoupes(name, responsable, base_ip, base_mask, mode, value)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            with self._connect() as c:
                cur = c.execute(sql, (
                    (name or "").strip(),
                    (responsable or "Anonyme"),
                    base_ip,
                    base_mask,
                    mode,
                    value,
                ))
                return cur.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Impossible d’enregistrer : {e}")

    # --- le reste inchangé ----------------------------------------------------
    def get_decoupe_by_id(self, decoupe_id: int) -> Optional[sqlite3.Row]:
        with self._connect() as c:
            row = c.execute("SELECT * FROM decoupes WHERE id = ?", (decoupe_id,)).fetchone()
            return row

    def get_decoupe_by_name(self, name: str) -> Optional[sqlite3.Row]:
        with self._connect() as c:
            return c.execute("SELECT * FROM decoupes WHERE name = ?", (name,)).fetchone()

    def list_decoupes(self) -> list[sqlite3.Row]:
        with self._connect() as c:
            return c.execute("SELECT * FROM decoupes ORDER BY created_at DESC").fetchall()

    def list_by_responsable(self, responsable: str) -> list[sqlite3.Row]:
        with self._connect() as c:
            return c.execute(
                "SELECT * FROM decoupes WHERE responsable = ? ORDER BY created_at DESC",
                (responsable,)
            ).fetchall()

    def delete_decoupe(self, decoupe_id: int) -> None:
        with self._connect() as c:
            c.execute("DELETE FROM decoupes WHERE id = ?", (decoupe_id,))

    def bulk_insert_subnets(self, decoupe_id: int, subnets: Iterable[Dict]) -> None:
        sql =  """
            INSERT OR IGNORE INTO subnets(decoupe_id, network_ip, mask, first_host, last_host, broadcast, nb_ip)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with self._connect() as c:
            c.executemany(sql, [
                (decoupe_id, s["network_ip"], s["mask"], s["first_host"], s["last_host"], s["broadcast"], int(s["nb_ip"]))
                for s in subnets
            ])

    def list_subnets(self, decoupe_id: int) -> list[sqlite3.Row]:
        with self._connect() as c:
            return c.execute(
                "SELECT * FROM subnets WHERE decoupe_id = ? ORDER BY network_ip",
                (decoupe_id,)
            ).fetchall()
