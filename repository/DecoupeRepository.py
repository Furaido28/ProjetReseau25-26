# repository/DecoupeRepository.py
import sqlite3
from typing import Iterable, Dict, Optional

class DecoupeRepository:
    def __init__(self, security):
        """
        security: instance de SecurityManager (root.security)
        """
        self.security = security  # on réutilise SA connexion
        self.conn = security.conn
        self.cur = self.conn.cursor()

    # plus de _connect() ici !

    def insert_decoupe(
        self, *, name: str, responsable: Optional[str], base_ip: str, base_mask: str, mode: str, value: str) -> int:
        sql = """
            INSERT INTO decoupes(name, responsable, base_ip, base_mask, mode, value)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cur = self.cur.execute(sql, (
            (name or "").strip(),
            (responsable or "Anonyme"),
            base_ip,
            base_mask,
            mode,
            value,
        ))
        self.conn.commit()
        return cur.lastrowid

    def get_decoupe_by_id(self, decoupe_id: int) -> Optional[sqlite3.Row]:
        return self.cur.execute(
            "SELECT * FROM decoupes WHERE id = ?", (decoupe_id,)
        ).fetchone()

    def get_decoupe_by_name(self, name: str) -> Optional[sqlite3.Row]:
        return self.cur.execute(
            "SELECT * FROM decoupes WHERE name = ?", (name,)
        ).fetchone()

    def list_decoupe(self) -> list[sqlite3.Row]:
        return self.cur.execute(
            "SELECT * FROM decoupes ORDER BY created_at DESC"
        ).fetchall()

    def list_by_responsable(self, responsable: str) -> list[sqlite3.Row]:
        return self.cur.execute(
            "SELECT * FROM decoupes WHERE responsable = ? ORDER BY created_at DESC",
            (responsable,)
        ).fetchall()

    def delete_decoupe(self, decoupe_id: int) -> None:
        self.cur.execute("DELETE FROM decoupes WHERE id = ?", (decoupe_id,))
        self.conn.commit()

    def bulk_insert_subnets(self, decoupe_id: int, subnets: Iterable[Dict]) -> None:
        sql =  """
            INSERT OR IGNORE INTO subnets(decoupe_id, network_ip, mask, first_host, last_host, broadcast, nb_ip)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.cur.executemany(sql, [
            (decoupe_id, s["network_ip"], s["mask"], s["first_host"], s["last_host"], s["broadcast"], int(s["nb_ip"]))
            for s in subnets
        ])
        self.conn.commit()

    def list_subnets(self, decoupe_id: int) -> list[sqlite3.Row]:
        return self.cur.execute(
            "SELECT * FROM subnets WHERE decoupe_id = ? ORDER BY network_ip",
            (decoupe_id,)
        ).fetchall()

    def update_decoupe(self, decoupe_id: int, *, base_mask: str, value: str, mode: str) -> None:
        sql = """
            UPDATE decoupes
               SET base_mask = ?,
                   value     = ?,
                   mode      = ?
             WHERE id = ?
        """
        cur = self.cur.execute(sql, (base_mask, value, mode, decoupe_id))
        self.conn.commit()
        if cur.rowcount == 0:
            raise ValueError(f"Aucune découpe trouvée avec l'ID {decoupe_id}")