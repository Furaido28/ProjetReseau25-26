# repository/DecoupeRepository.py
import sqlite3
from typing import Iterable, Dict, Optional
from models.Decoupe import Decoupe

# + imports pour rendre le chemin robuste
from pathlib import Path
import sys

class DecoupeRepository:
    def __init__(self, db_path: str = None):
        # Base = dossier du fichier courant (compatible PyInstaller)
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        if db_path is None:
            # ../bdd/projetReseau.db par rapport à CE fichier
            self.db_path = (base_dir / ".." / "bdd" / "projetReseau.db").resolve()
        else:
            self.db_path = Path(db_path).resolve()

        # S’assurer que le dossier existe
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self):
        # sqlite créera le fichier si non présent, mais le dossier doit exister
        conn = sqlite3.connect(str(self.db_path), timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  # indispensable pour ON DELETE CASCADE
        return conn

    # --- DECoupes -------------------------------------------------------------
    def insert_decoupe(self, d: Decoupe) -> int:
        """Insère une découpe et renvoie son id SQLite."""
        sql = """
        INSERT INTO decoupes(name, responsable, base_ip, base_mask, mode, value)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            with self._connect() as c:
                cur = c.execute(sql, (
                    d.get_name(),
                    d.get_responsable_name() or "Anonyme",
                    d.get_base_ip(),
                    d.get_base_mask(),
                    d.get_mode(),
                    d.get_value(),  # << 6e valeur correspondant à 'value'
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
