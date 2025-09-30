# models/DecoupeRepository.py
import sqlite3
from typing import Iterable, Dict, Optional
from models.Decoupe import Decoupe

class DecoupeRepository:
    def __init__(self, db_path: str = "../bdd/projetReseau.db"):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  # indispensable pour ON DELETE CASCADE
        return conn

    # --- DECoupes -------------------------------------------------------------
    def insert_decoupe(self, d: Decoupe) -> int:
        """Insère une découpe et renvoie son id SQLite."""
        sql = """
        INSERT INTO decoupes(name, responsable, base_ip, base_mask, mode)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            with self._connect() as c:
                cur = c.execute(sql, (
                    d.get_name(),
                    d.get_responsable_name() or "Anonyme",
                    d.get_base_ip(),
                    d.get_base_mask(),
                    d.get_mode() or "classless",
                ))
                return cur.lastrowid
        except sqlite3.IntegrityError as e:
            # name est UNIQUE dans ton schéma
            raise ValueError(f"Impossible d’enregistrer : {e}")

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
        """Supprime la découpe et ses subnets (grâce au ON DELETE CASCADE)."""
        with self._connect() as c:
            c.execute("DELETE FROM decoupes WHERE id = ?", (decoupe_id,))

    # --- SUBNETS --------------------------------------------------------------
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