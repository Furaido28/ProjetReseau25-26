import sqlite3

class DatabaseManager:
    """
    Classe pour gérer les interactions avec la base de données.
    """
    def __init__(self, db_path="bdd/projetReseau.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # accès aux colonnes par nom
        self.cursor = self.conn.cursor()

    # -----------------------------
    # Gestion du mot de passe global
    # -----------------------------
    def get_password(self):
        self.cursor.execute("SELECT password FROM settings LIMIT 1")
        row = self.cursor.fetchone()
        return row["password"] if row else None

    def set_password(self, pwd: str):
        self.cursor.execute("DELETE FROM settings")  # garde un seul mot de passe
        self.cursor.execute("INSERT INTO settings(password) VALUES (?)", (pwd,))
        self.conn.commit()

    def has_password(self) -> bool:
        return self.get_password() is not None

    def check_password(self, password: str) -> bool:
        db_pwd = self.get_password()
        return db_pwd is not None and db_pwd == password

    # -----------------------------
    # Fermeture
    # -----------------------------
    def close(self):
        self.conn.close()
